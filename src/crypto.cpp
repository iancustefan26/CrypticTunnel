#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <iostream>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

void free_all(RSA* rsa, BIGNUM* bne, BIO* bp_public, BIO* bp_private){
    if (bne) BN_free(bne);
    if (rsa) RSA_free(rsa);
    if (bp_public) BIO_free_all(bp_public);
    if (bp_private) BIO_free_all(bp_private);
}

std::pair<std::string, std::string> generateRSAKeyPair() {
    std::pair<std::string, std::string> keyPair;
    RSA *rsa = nullptr;
    BIGNUM *bne = nullptr;
    BIO *bp_public = nullptr, *bp_private = nullptr;
    int bits = 2048;
    unsigned long e = RSA_F4;

    bne = BN_new();
    if (!BN_set_word(bne, e)) {
        std::cerr << "Error setting RSA exponent" << std::endl;
        free_all(rsa,bne,bp_public, bp_private);
        return std::pair<std::string, std::string>("", "");
    }

    rsa = RSA_new();
    if (!RSA_generate_key_ex(rsa, bits, bne, nullptr)) {
        std::cerr << "Error generating RSA key" << std::endl;
        free_all(rsa,bne,bp_public, bp_private);
        return std::pair<std::string, std::string>("", "");
    }

    bp_public = BIO_new(BIO_s_mem());
    if (!PEM_write_bio_RSAPublicKey(bp_public, rsa)) {
        std::cerr << "Error writing RSA public key" << std::endl;
        free_all(rsa,bne,bp_public, bp_private);
        return std::pair<std::string, std::string>("", "");
    }

    bp_private = BIO_new(BIO_s_mem());
    if (!PEM_write_bio_RSAPrivateKey(bp_private, rsa, nullptr, nullptr, 0, nullptr, nullptr)) {
        // Handle error
        std::cerr << "Error writing RSA private key" << std::endl;
        free_all(rsa,bne,bp_public, bp_private);
        return std::pair<std::string, std::string>("", "");
    }

    char *pub_key_ptr = nullptr;
    long pub_key_len = BIO_get_mem_data(bp_public, &pub_key_ptr);
    keyPair.first = std::string(pub_key_ptr, pub_key_len);

    char *priv_key_ptr = nullptr;
    long priv_key_len = BIO_get_mem_data(bp_private, &priv_key_ptr);
    keyPair.second = std::string(priv_key_ptr, priv_key_len);

    return keyPair;
}


int main() {
    std::pair<std::string, std::string> key_pair = generateRSAKeyPair();

    std::cout << key_pair.first << "\n" << key_pair.second;

    return 0;
}


#pragma GCC diagnostic pop
