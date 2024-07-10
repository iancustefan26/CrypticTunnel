
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rand.h>
#include <iostream>
#include <vector>
#include <cstring>
#include <string>
#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

using namespace std;
namespace py = pybind11;

void handleErrors() {
    cerr << "Error with AES operations";
    abort();
}

vector<unsigned char> stringToVector(const string& str) {
    return vector<unsigned char>(str.begin(), str.end());
}

string vectorToHexString(const vector<unsigned char>& vec) {
    string hex_str;
    for (unsigned char c : vec) {
        char buf[3];
        snprintf(buf, sizeof(buf), "%02x", c);
        hex_str.append(buf);
    }
    return hex_str;
}

std::vector<unsigned char> hexStringToVector(const std::string& hex_str) {
    if (hex_str.length() % 2 != 0) {
        throw std::invalid_argument("Hex string must have an even number of characters");
    }
    std::vector<unsigned char> vec;
    vec.reserve(hex_str.length() / 2);

    for (size_t i = 0; i < hex_str.length(); i += 2) {
        std::string byteString = hex_str.substr(i, 2);
        unsigned char byte = static_cast<unsigned char>(stoi(byteString, nullptr, 16));
        vec.push_back(byte);
    }

    return vec;
}

string aes_encrypt(const string& plaintext, const string& key, const string& iv) {
    EVP_CIPHER_CTX* ctx;
    vector<unsigned char> ciphertext(plaintext.size() + AES_BLOCK_SIZE);
    int len;
    int ciphertext_len;

    if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, hexStringToVector(key).data(), hexStringToVector(iv).data())) handleErrors();

    if(1 != EVP_EncryptUpdate(ctx, ciphertext.data(), &len, (unsigned char*)plaintext.data(), plaintext.size())) handleErrors();
    ciphertext_len = len;

    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len)) handleErrors();
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    ciphertext.resize(ciphertext_len);
    return vectorToHexString(ciphertext);
}

string aes_decrypt(const string& ciphertext, const string& key, const string& iv) {
    EVP_CIPHER_CTX* ctx;
    vector<unsigned char> plaintext(ciphertext.size());
    int len;
    int plaintext_len;

    if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, hexStringToVector(key).data(), hexStringToVector(iv).data())) handleErrors();

    if(1 != EVP_DecryptUpdate(ctx, plaintext.data(), &len, hexStringToVector(ciphertext).data(), hexStringToVector(ciphertext).size())) handleErrors();
    plaintext_len = len;

    if(1 != EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len)) handleErrors();
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    plaintext.resize(plaintext_len);
    return vectorToHexString(plaintext);
}
/*
int main() {
    vector<unsigned char> key(32); 
    vector<unsigned char> iv(AES_BLOCK_SIZE);

    if (!RAND_bytes(key.data(), key.size())) handleErrors();
    if (!RAND_bytes(iv.data(), iv.size())) handleErrors();

    string plaintext = "This is a secret message.";

    vector<unsigned char> encrypted = aes_encrypt(plaintext, key, iv);
    string key_hex = vectorToHexString(key);
    string iv_hex = vectorToHexString(iv);
    string encrypted_hex = vectorToHexString(encrypted);
    cout << "Original: " << plaintext << endl;
    cout << "Key (hex): " << key_hex << endl;
    cout << "IV (hex): " << iv_hex << endl;
    cout << "Encrypted (hex): " << encrypted_hex << endl;

    vector<unsigned char> decrypted = aes_decrypt(encrypted, key, iv);

    cout << "Decrypted: " << vectorToHexString(decrypted);

    return 0;
}
*/
PYBIND11_MODULE(aeslib, m){
    m.doc() = "AES functions";

    m.def("aes_encrypt", &aes_encrypt, "Funtion that encrypts a plaintext using a key AES256 (plain, key, iv)");
    m.def("aes_decrypt", &aes_decrypt, "Funtion that decrypts a cipher using a key AES256 (cipher, key, iv)");

}

#pragma GCC diagnostic pop
