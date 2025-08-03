# Centralized UPI Payment Gateway

A secure, blockchain-integrated UPI payment system implementing Lightweight Cryptography (LWC), Quantum Cryptography simulation, and SHA-256 hashing for enhanced transaction security.

## 🏗️ System Architecture

This project simulates a complete digital transaction ecosystem using three distinct entities:

- **UPI Machine**: Central processing unit mimicking merchant sound-box machines
- **User Platform**: Client interface for payment initiation via QR code scanning
- **Bank Terminal**: Banking server for transaction validation and processing

## 🔐 Security Features

### Lightweight Cryptography (LWC)
- **SPECK Algorithm**: High-speed encryption for resource-constrained environments
- **Virtual Merchant ID (VMID)** generation from Merchant ID and timestamp
- **QR Code Encryption** for secure merchant identification

### Blockchain Integration
- **Immutable Transaction Ledger** maintained by each bank
- **Transaction Block Structure**:
  - Transaction ID (Hash of UID, MID, Timestamp, Amount)
  - Previous Block Hash
  - Timestamp
- **Transparent and Verifiable** transaction history

### Quantum Cryptography Simulation
- **Shor's Algorithm Implementation** to demonstrate PIN vulnerabilities
- **Classical Cryptography Vulnerability Assessment**
- **Quantum-resistant Security Analysis**

## 🏦 Banking System

### Registration Process
- **Merchant Registration**: Name, IFSC Code, Password, Initial Balance
- **User Registration**: Similar to merchant + PIN setup for UPI transactions
- **Unique ID Generation**: 16-digit hexadecimal numbers using SHA-256 hashing

## 🔄 Transaction Flow

1. **Merchant Registration** → Bank generates 16-digit Merchant ID (MID)
2. **QR Code Generation** → UPI Machine encrypts MID using LWC
3. **User Scans QR Code** → Provides MMID, amount, and PIN
4. **Transaction Processing** → UPI Machine decrypts and forwards to bank
5. **Bank Validation** → Verifies credentials and available balance
6. **Blockchain Recording** → Valid transactions stored immutably
7. **Fund Transfer** → Completion notification to all parties

## 🛠️ Technical Implementation

### Cryptographic Algorithms
- **SHA-256**: Merchant/User ID generation and transaction hashing
- **SPECK**: Lightweight encryption for VMID generation
- **Shor's Algorithm**: Quantum cryptography vulnerability simulation

### Data Structures
- **Blockchain Ledger**: Linked list of transaction blocks
- **User Database**: MMID, PIN, account details
- **Merchant Database**: MID, account information, transaction history

## 🔍 Key Features Demonstration

### Lightweight Cryptography
- Fast VMID generation using SPECK algorithm
- Minimal computational overhead for mobile devices
- Secure QR code encryption/decryption

### Quantum Vulnerability Analysis
- Shor's algorithm simulation on user PINs
- Demonstrates classical cryptography weaknesses
- Quantum-resistant recommendations

### Blockchain Security
- Immutable transaction recording
- Distributed ledger across bank branches
- Cryptographic hash chaining for integrity

## 📊 Performance Metrics

- **Transaction Processing Time**: < 2 seconds
- **QR Code Generation**: < 500ms
- **Blockchain Block Creation**: < 1 second
- **Encryption/Decryption**: < 100ms

## 🛡️ Security Considerations

### Implemented Security Measures
- Multi-layer encryption (SHA-256 + SPECK)
- Blockchain immutability
- PIN validation with quantum vulnerability assessment
- Secure communication between entities

### Known Vulnerabilities
- Classical PIN encryption susceptible to quantum attacks
- Centralized architecture single point of failure
- QR code interception possibilities

## 🔮 Future Enhancements

- **Post-Quantum Cryptography** integration
- **Decentralized Architecture** implementation
- **Multi-signature Transactions** support
- **Advanced Fraud Detection** using ML
- **Cross-bank Interoperability** enhancement
