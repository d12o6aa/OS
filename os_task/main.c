#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <errno.h>

// Function prototypes
void displayMenu();
void listFilesAndDirectories(const char *path);
void changeFilePermissions(const char *filename, mode_t mode);
void createFile(const char *filename);
void deleteFile(const char *filename);
void createDirectory(const char *dirname);
void deleteDirectory(const char *dirname);
void createSymbolicLink(const char *target, const char *linkname);

int main() {
    char *path = "../"; // Current directory
    int choice;

    do {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                listFilesAndDirectories(path);
                break;
            case 2:
                // B. Change permissions of files
                // This option requires the user to input a filename and new permissions
                // For simplicity, I'm not implementing input validation here
                {
                    char filename[100];
                    mode_t new_permissions;
                    printf("Enter filename: ");
                    scanf("%s", filename);
                    printf("Enter new permissions (in octal): ");
                    scanf("%o", &new_permissions);
                    changeFilePermissions(filename, new_permissions);
                }
                break;
            case 3:
                // C. Make/delete files/directories
                // This option requires the user to input a filename/directory name
                // For simplicity, I'm not implementing input validation here
                {
                    char filename[100];
                    printf("Enter filename/directory name: ");
                    scanf("%s", filename);
                    createFile(filename);
                    deleteFile(filename);
                    createDirectory(filename);
                    deleteDirectory(filename);
                }
                break;
            case 4:
                // D. Create symbolic link files
                // This option requires the user to input a target file and link name
                // For simplicity, I'm not implementing input validation here
                {
                    char target_file[100], symbolic_link[100];
                    printf("Enter target file: ");
                    scanf("%s", target_file);
                    printf("Enter symbolic link name: ");
                    scanf("%s", symbolic_link);
                    createSymbolicLink(target_file, symbolic_link);
                }
                break;
            case 5:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Please enter a number between 1 and 5.\n");
        }
    } while (choice != 5);

    return 0;
}

void displayMenu() {
    printf("\nFile Manager Menu\n");
    printf("1. List files/directories\n");
    printf("2. Change permissions of files\n");
    printf("3. Make/delete files/directories\n");
    printf("4. Create symbolic link files\n");
    printf("5. Exit\n");
}

void listFilesAndDirectories(const char *path) {
    DIR *dir;
    struct dirent *entry;

    dir = opendir(path);
    if (dir == NULL) {
        perror("Unable to open directory");
        return;
    }

    printf("Files and directories in %s:\n", path);
    while ((entry = readdir(dir)) != NULL) {
        printf("%s\n", entry->d_name);
    }

    closedir(dir);
}

void changeFilePermissions(const char *filename, mode_t mode) {
    if (chmod(filename, mode) == -1) {
        perror("Unable to change file permissions");
        return;
    }
    printf("Permissions changed for %s\n", filename);
}

void createFile(const char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Unable to create file");
        return;
    }
    fclose(file);
    printf("File created: %s\n", filename);
}

void deleteFile(const char *filename) {
    if (remove(filename) == -1) {
        perror("Unable to delete file");
        return;
    }
    printf("File deleted: %s\n", filename);
}

void createDirectory(const char *dirname) {
    if (mkdir(dirname, 0777) == -1) {
        perror("Unable to create directory");
        return;
    }
    printf("Directory created: %s\n", dirname);
}

void deleteDirectory(const char *dirname) {
    if (rmdir(dirname) == -1) {
        perror("Unable to delete directory");
        return;
    }
    printf("Directory deleted: %s\n", dirname);
}

void createSymbolicLink(const char *target, const char *linkname) {
    if (symlink(target, linkname) == -1) {
        perror("Unable to create symbolic link");
        return;
    }
    printf("Symbolic link created: %s -> %s\n", linkname, target);
}
