#M-A-SCc
#C-Modul for soon to be Adlist-Sanitizer 0.02b

#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

// Callback-Function for download
size_t schreib_callback(void* daten, size_t groesse, size_t anzahl, void* stream) {
    FILE* datei = (FILE*)stream;
    return fwrite(daten, groesse, anzahl, datei);
}

int main() {
    // URL and downloadpath
    const char* url = "http://www.example.com/example.txt";
    const char* ziel = "downloads/example.txt";

    // Curl-Initialising
    CURL* curl = curl_easy_init();
    if (curl == NULL) {
        printf("Fehler beim Initialisieren von libcurl.\n");
        return 1;
    }

    // Targetfile
    FILE* datei = fopen(ziel, "wb");
    if (datei == NULL) {
        printf("Error opening file.\n");
        curl_easy_cleanup(curl);
        return 1;
    }

    // libcurl-config
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, schreib_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, datei);

    // Star download
    CURLcode ergebnis = curl_easy_perform(curl);

    // Ress
    fclose(datei);
    curl_easy_cleanup(curl);

    if (result != CURLE_OK) {
        printf("Error trying to download file: %s\n", curl_easy_strerror(ergebnis));
        return 1;
    }

    printf("download successfully!\n");

    return 0;
}
