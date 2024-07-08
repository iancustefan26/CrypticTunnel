
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/rand.h>
#include <iostream>
#include <vector>
#include <cstring>
#include <string>

using namespace std;

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

vector<unsigned char> aes_encrypt(const string& plaintext, const vector<unsigned char>& key, const vector<unsigned char>& iv) {
    EVP_CIPHER_CTX* ctx;
    vector<unsigned char> ciphertext(plaintext.size() + AES_BLOCK_SIZE);
    int len;
    int ciphertext_len;

    if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key.data(), iv.data())) handleErrors();

    if(1 != EVP_EncryptUpdate(ctx, ciphertext.data(), &len, (unsigned char*)plaintext.data(), plaintext.size())) handleErrors();
    ciphertext_len = len;

    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len)) handleErrors();
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    ciphertext.resize(ciphertext_len);
    return ciphertext;
}

vector<unsigned char> aes_decrypt(const vector<unsigned char>& ciphertext, const vector<unsigned char>& key, const vector<unsigned char>& iv) {
    EVP_CIPHER_CTX* ctx;
    vector<unsigned char> plaintext(ciphertext.size());
    int len;
    int plaintext_len;

    if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key.data(), iv.data())) handleErrors();

    if(1 != EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size())) handleErrors();
    plaintext_len = len;

    if(1 != EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len)) handleErrors();
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    plaintext.resize(plaintext_len);
    return plaintext;
}

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
