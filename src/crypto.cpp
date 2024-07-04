#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <utility>
#include <locale>
#include <codecvt>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <stdio.h>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

using namespace std;
namespace py = pybind11;

std::string string_to_utf8(const std::string& str) {
    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    std::wstring wide = std::wstring(str.begin(), str.end());
    return converter.to_bytes(wide); 
}

std::string string_to_hex(const std::string& input) {
    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    for (size_t i = 0; i < input.length(); ++i) {
        ss << "\\x" << std::setw(2) << static_cast<unsigned>(static_cast<unsigned char>(input[i]));
    }
    return ss.str();
}

void free_all(RSA* rsa, BIGNUM* bne, BIO* bp_public, BIO* bp_private){
    if (bne) BN_free(bne);
    if (rsa) RSA_free(rsa);
    if (bp_public) BIO_free_all(bp_public);
    if (bp_private) BIO_free_all(bp_private);
}

void free_enc(RSA* rsa, BIO* bio_p, char* encrypted_message){
    if(rsa)
        RSA_free(rsa);
    if(bio_p)
        BIO_free(bio_p);
    if(encrypted_message)
        delete[] encrypted_message;
}

pair<std::string, std::string> generateRSAKeyPair() {
    pair<string, string> keyPair;
    RSA *rsa = nullptr;
    BIGNUM *bne = nullptr;
    BIO *bp_public = nullptr, *bp_private = nullptr;
    int bits = 2048;
    unsigned long e = RSA_F4;

    bne = BN_new();
    if (!BN_set_word(bne, e)) {
        cerr << "\nError setting RSA exponent: ";
        free_all(rsa,bne,bp_public, bp_private);
        return pair<string, string>("", "");
    }

    rsa = RSA_new();
    if (!RSA_generate_key_ex(rsa, bits, bne, nullptr)) {
        std::cerr << "\nError generating RSA key: ";
        free_all(rsa,bne,bp_public, bp_private);
        return pair<string, string>("", "");
    }

    bp_public = BIO_new(BIO_s_mem());
    if (!PEM_write_bio_RSAPublicKey(bp_public, rsa)) {
        cerr << "\nError writing RSA public key; ";
        free_all(rsa,bne,bp_public, bp_private);
        return std::pair<string, string>("", "");
    }

    bp_private = BIO_new(BIO_s_mem());
    if (!PEM_write_bio_RSAPrivateKey(bp_private, rsa, nullptr, nullptr, 0, nullptr, nullptr)) {
        cerr << "\nError writing RSA private key: ";
        free_all(rsa,bne,bp_public, bp_private);
        return ::pair<string, string>("", "");
    }

    char *pub_key_ptr = nullptr;
    long pub_key_len = BIO_get_mem_data(bp_public, &pub_key_ptr);
    keyPair.first = string(pub_key_ptr, pub_key_len);

    char *priv_key_ptr = nullptr;
    long priv_key_len = BIO_get_mem_data(bp_private, &priv_key_ptr);
    keyPair.second = string(priv_key_ptr, priv_key_len);

    return keyPair;
}

string rsa_encrypt(string &plain, const string& public_key){
    RSA* rsa = nullptr;
    BIO* bio_p = nullptr;
    string cipher;

    bio_p = BIO_new_mem_buf((void*)public_key.c_str(), -1);
    if(! bio_p){
        cerr << "\nError creating BIO: ";
        free_enc(rsa, bio_p, nullptr);
    }
    rsa = PEM_read_bio_RSAPublicKey(bio_p, nullptr, nullptr, nullptr);
    if(!rsa){
        cerr << "\nError loading RSA Public Key: ";
        free_enc(rsa, bio_p, nullptr);
    }
    int rsa_len = RSA_size(rsa);
    unsigned char* encrypted_message = new unsigned char[rsa_len + 1];
    int enc_message_length = RSA_public_encrypt(
        plain.length(),
        (const unsigned char*)plain.c_str(),
        encrypted_message,
        rsa,
        RSA_PKCS1_PADDING
    );
    if(enc_message_length == -1){
        cerr << "\nError encrypting message with the public key: ";
        free_enc(rsa, bio_p, reinterpret_cast<char*>(encrypted_message));
    }

    cipher = string((char*)encrypted_message, enc_message_length);
    string file_name = "temp.bin";
    ofstream output(file_name, std::ios::out | std::ios::app);
    output << cipher;
    output.close();

    return file_name;
}

string rsa_decrypt(const string private_key){
    RSA* rsa;
    BIO* bio_p;
    string plain;
    string cipher;
    ifstream input("transfered/temp.bin");
    ostringstream oss;
    oss << input.rdbuf();
    cipher = oss.str();
    input.close();
    bio_p = BIO_new_mem_buf((void*)private_key.c_str(), -1);
    if(!bio_p){
        cerr << "Error when loading private key into BIO: \n";
        free_enc(rsa, bio_p, nullptr);
    }

    rsa = PEM_read_bio_RSAPrivateKey(bio_p, nullptr, nullptr, nullptr);
    if(!rsa){
        cerr << "\nError loading private key from BIO: \n";
        free_enc(rsa, bio_p, nullptr);
    }

    int rsa_len = RSA_size(rsa);
    unsigned char* decryted_message = new unsigned char[rsa_len + 1];
    int decr_message_length = RSA_private_decrypt(
        cipher.length(),
        (const unsigned char*)cipher.c_str(),
        decryted_message,
        rsa,
        RSA_PKCS1_PADDING
    );
    if (decr_message_length == -1) {
        cerr << "Error when decrypting cipher: " << ERR_error_string(ERR_get_error(), nullptr) << "\n";
        free_enc(rsa, bio_p, reinterpret_cast<char*>(decryted_message));
        return "";
    }

    plain = string((char*)decryted_message, decr_message_length);

    return plain;
}
int method(int x){
    cout << x * 2;
    return 0;
}

void test_method(const string param){
    cout << param;
}

PYBIND11_MODULE(rsalib, m){
    m.doc() = "RSA functions";

    m.def("rsa_decrypt", &rsa_decrypt, "Function that decrypts a RSA cipher using the private key");
    m.def("rsa_encrypt", &rsa_encrypt, "Function that encrypts a plaintext using a public key");
    m.def("generateRSAKeyPair", &generateRSAKeyPair, "Function that returns a tuple for RSA keys <public_key, private_key");
    m.def("method", &method, "A test function ; (int)");
    m.def("test_string", &test_method, "Method to test string pass");

}


#pragma GCC diagnostic pop
