#include <stdio.h>
#include <stdlib.h>

int main() {
    // Get platform-appropriate information
    printf("Hello from Ono!\n");
    printf("User home directory: %s\n", "<?ono get user home directory ?>");
    printf("System temp directory: %s\n", "<?ono get system temp directory ?>");
    
    // Create a file in the temp directory
    FILE *fp = fopen("<?ono get temp directory ?>/hello_ono.txt", "w");
    if (fp != NULL) {
        fprintf(fp, "Ono C example\n");
        fclose(fp);
    }
    
    return 0;
}