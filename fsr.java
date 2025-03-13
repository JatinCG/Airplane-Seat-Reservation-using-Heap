package ch1;

import java.util.Scanner;

public class fsr {

    // Constants for seat counts
    private static final int ECONOMY_SEATS = 10;
    private static final int BUSINESS_SEATS = 5;
    private static final int OVERBOOK_LIMIT = 2; // Allow 2 overbookings

    // Arrays to store seats and standby list
    private static String[] economySeats = new String[ECONOMY_SEATS];
    private static String[] businessSeats = new String[BUSINESS_SEATS];
    private static String[] standbyList = new String[ OVERBOOK_LIMIT];
    private static int standbyCount = 0;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("\n1. Reserve Seat");
            System.out.println("2. View Seats");
            System.out.println("3. Exit");
            System.out.print("Choose an option: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline

            switch (choice) {
                case 1:
                    reserveSeat(scanner);
                    break;
                case 2:
                    viewSeats();
                    break;
                case 3:
                    System.out.println("Exiting...");
                    scanner.close();
                    return;
                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }
    }

    private static void reserveSeat(Scanner scanner) {
        System.out.print("Enter passenger name: ");
        String name = scanner.nextLine();

        System.out.print("Choose class (1 for Economy, 2 for Business): ");
        int classChoice = scanner.nextInt();
        scanner.nextLine(); // Consume newline

        if (classChoice == 1) {
            if (reserveEconomySeat(name)) {
                System.out.println("Economy seat reserved for " + name);
            } else {
                System.out.println("Economy class is full. Added to standby list.");
                addToStandbyList(name);
            }
        } else if (classChoice == 2) {
            if (reserveBusinessSeat(name)) {
                System.out.println("Business seat reserved for " + name);
            } else {
                System.out.println("Business class is full. Added to standby list.");
                addToStandbyList(name);
            }
        } else {
            System.out.println("Invalid class choice.");
        }
    }

    private static boolean reserveEconomySeat(String name) {
        for (int i = 0; i < ECONOMY_SEATS; i++) {
            if (economySeats[i] == null) {
                economySeats[i] = name;
                return true;
            }
        }
        return false; // No available seats
    }

    private static boolean reserveBusinessSeat(String name) {
        for (int i = 0; i < BUSINESS_SEATS; i++) {
            if (businessSeats[i] == null) {
                businessSeats[i] = name;
                return true;
            }
        }
        return false; // No available seats
    }

    private static void addToStandbyList(String name) {
        if (standbyCount < standbyList.length) {
            standbyList[standbyCount] = name;
            standbyCount++;
        } else {
            System.out.println("Standby list is full. Cannot add more passengers.");
        }
    }

    public static void viewSeats() {
        System.out.println("\nEconomy Class Seats:");
        for (int i = 0; i < ECONOMY_SEATS; i++) {
            System.out.println("Seat " + (i + 1) + ": " + (economySeats[i] != null ? economySeats[i] : "Available"));
        }

        System.out.println("\nBusiness Class Seats:");
        for (int i = 0; i < BUSINESS_SEATS; i++) {
            System.out.println("Seat " + (i + 1) + ": " + (businessSeats[i] != null ? businessSeats[i] : "Available"));
        }

        System.out.println("\nStandby List:");
        if (standbyCount == 0) {
            System.out.println("No passengers on standby.");
        } else {
            for (int i = 0; i < standbyCount; i++) {
                System.out.println(standbyList[i]);
            }
        }
    }
}
