#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <errno.h>

void displayMenu(void);
void displayMenu2(void);
void listFilesAndDirectories(const char *path);
void changeFilePermissions(const char *filename, mode_t mode);
void createFile(const char *filename);
void deleteFile(const char *filename);
void createDirectory(const char *dirname);
void deleteDirectory(const char *dirname);
void createSymbolicLink(const char *target, const char *linkname);

/**
 * main - main function
 *
 * Retun : int 
*/

int main(void)
{
    char *path = "../"; 
    int choice,choice2;

    do {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                listFilesAndDirectories(path);
                break;
            case 2:
                
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
                
                {
                    char filename[100];
                    char directoryename[100];
                    displayMenu2();
                    printf("Enter your choice: ");
                    scanf("%d", &choice2);
                    switch (choice2)
                    {
                    case 1:
                        printf("Enter filename: ");
                        scanf("%s", filename);
                        createFile(filename);
                        break;
                    case 2:
                        printf("Enter directory name: ");
                        scanf("%s", directoryename);
                        createDirectory(directoryename);
                        break;
                    case 3:
                        printf("Enter filename: ");
                        scanf("%s", filename);
                        deleteFile(filename);
                        break;
                    
                    case 4:
                        printf("Enter directory name: ");
                        scanf("%s", directoryename);
                        deleteDirectory(directoryename);
                        break;

                    default:
                        break;
                    }
                    
                }
                break;
            case 4:
                
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

void displayMenu2() {
    printf("1. Make files\n");
    printf("2. Make directories\n");
    printf("3. Delete files\n");
    printf("4. Delete sdirectories\n");
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
