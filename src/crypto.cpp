#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <iostream>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

using namespace std;

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
        delete encrypted_message;
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
        cerr << "Error setting RSA exponent: ";
        free_all(rsa,bne,bp_public, bp_private);
        return pair<string, string>("", "");
    }

    rsa = RSA_new();
    if (!RSA_generate_key_ex(rsa, bits, bne, nullptr)) {
        std::cerr << "Error generating RSA key: ";
        free_all(rsa,bne,bp_public, bp_private);
        return pair<string, string>("", "");
    }

    bp_public = BIO_new(BIO_s_mem());
    if (!PEM_write_bio_RSAPublicKey(bp_public, rsa)) {
        cerr << "Error writing RSA public key; ";
        free_all(rsa,bne,bp_public, bp_private);
        return std::pair<string, string>("", "");
    }

    bp_private = BIO_new(BIO_s_mem());
    if (!PEM_write_bio_RSAPrivateKey(bp_private, rsa, nullptr, nullptr, 0, nullptr, nullptr)) {
        cerr << "Error writing RSA private key: ";
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

string rsa_encrypt(const string &plain, const string public_key){
    RSA* rsa = nullptr;
    BIO* bio_p = nullptr;
    string cipher;

    bio_p = BIO_new_mem_buf((void*)public_key.c_str(), -1);
    if(! bio_p){
        cerr << "Error creating BIO: ";
        free_enc(rsa, bio_p, nullptr);
    }
    rsa = PEM_read_bio_RSAPublicKey(bio_p, nullptr, nullptr, nullptr);
    if(!rsa){
        cerr << "Error loading RSA Public Key: ";
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
        cerr << "Error encrypting message with the public key: ";
        free_enc(rsa, bio_p, reinterpret_cast<char*>(encrypted_message));
    }

    cipher = string((char*)encrypted_message, enc_message_length);

    return cipher;
}

string rsa_decrypt(const string &cipher, const string private_key){
    RSA* rsa;
    BIO* bio_p;
    string plain;

    bio_p = BIO_new_mem_buf((void*)private_key.c_str(), -1);
    if(!bio_p){
        cerr << "Error when loading private key into BIO: ";
        free_enc(rsa, bio_p, nullptr);
    }

    rsa = PEM_read_bio_RSAPrivateKey(bio_p, nullptr, nullptr, nullptr);
    if(!rsa){
        cerr << "Error loading private key from BIO: ";
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
    if(decr_message_length == -1){
        cerr << "Error when decrypting cipher: ";
        free_enc(rsa, bio_p, reinterpret_cast<char*>(decryted_message));
    }

    plain = string((char*)decryted_message, decr_message_length);

    return plain;
}

int main() {
    std::pair<std::string, std::string> key_pair = generateRSAKeyPair();

    std::cout << key_pair.first << "\n" << key_pair.second;

    string plain = "În 1996, o firmă privată din România a confecționat o monedă de probă"
    " - de fapt, un jeton -, destinată colecționarilor , având valoarea nominală";
    string enc_plain = rsa_encrypt(plain, key_pair.first);

    cout << enc_plain << "\n";

    string decrypted_plain = rsa_decrypt(enc_plain, key_pair.second);

    cout << decrypted_plain << "\n";


    return 0;
}


#pragma GCC diagnostic pop
