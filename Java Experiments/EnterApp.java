import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class EnterApp {
    static String path = "C:/Users/rodri/Documents/JavaStudy/Faro/src/login.txt";
    public static void main(String[] args) {
        enterIntoApp();
    }

    static void enterIntoApp() {

        Scanner input = new Scanner(System.in);
        int option;

        String menuText = ("""
            Menu:
            1. Login
            2. Signup
            """);
        do {
            System.out.println(menuText);
            System.out.print("Elige una opción: ");
            option = input.nextInt();
            input.nextLine(); // limpiar el salto de línea
        } while (option < 1 || option > 2);

        switch (option) {
            case 1 -> {
                boolean loginSuccessful = false;
                do {
                    System.out.print("Usuario: ");
                    String username = input.nextLine();
                    System.out.print("Contraseña: ");
                    String password = input.nextLine();

                    loginSuccessful = login(username, password);

                    if (!loginSuccessful) {
                        System.out.println("Incorrect username or password. Try again.\n");
                    }
                } while (!loginSuccessful);
                System.out.println("Login exitoso!");
            }
            case 2 -> {
                System.out.println("Signup...");
                signup();
            }
        }
    }

    static boolean login(String username, String password) {
        try (BufferedReader file = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = file.readLine()) != null) {
                String[] parts = line.split(":");
                if (parts.length == 2) {
                    String fileUsername = parts[0].trim();
                    String filePassword = parts[1].trim();
                    if (fileUsername.equals(username) && filePassword.equals(password)) {
                        return true;
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;
    }

    static void signup() {
        Scanner input = new Scanner(System.in);

        System.out.print("Elige un nombre de usuario: ");
        String newUsername = input.nextLine();

        // Verificar si ya existe
        if (usernameExists(newUsername)) {
            System.out.println("Este nombre de usuario ya está en uso. Intenta con otro.");
            return;
        }

        System.out.print("Elige una contraseña: ");
        String newPassword = input.nextLine();

        // Guardar en archivo
        try (FileWriter fw = new FileWriter(path, true)) {
            fw.write(newUsername + ":" + newPassword + "\n");
            System.out.println("¡Usuario registrado con éxito!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static boolean usernameExists(String username) {
        try (BufferedReader file = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = file.readLine()) != null) {
                String[] parts = line.split(":");
                if (parts.length > 0 && parts[0].trim().equals(username)) {
                    return true;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;
    }
}
