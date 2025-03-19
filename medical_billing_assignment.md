# Medical Center Billing System - Technical Interview Assignment

## Overview
Create a simplified version of a medical center billing system focusing on core billing functionality. This assignment evaluates your ability to implement essential features of a healthcare billing system while demonstrating clean code practices and proper architecture.


## Technical Requirements

### Preferred Technology Stack
- Backend: Django 4.x with Python 3.8+
- Database: PostgreSQL
- Frontend: Django Templates with Bootstrap 5
- JavaScript for client-side interactions
- Version Control: Git


## Core Features (Implement in this order)

### 1. Basic Patient Management
- Simple patient registration form (name, contact number, email)
- Generate unique patient ID
- List view of patients
- Basic search by name or ID

### 2. Simple Service Catalog
- Maintain a list of medical services with:
  - Service name
  - Base price
  - Status (active/inactive)
- Basic CRUD operations for services

### 3. Essential Billing
- Create a new bill by:
  - Selecting a patient
  - Adding 1-3 services
  - Calculating total
  - Applying a simple discount (percentage)
- Generate a basic bill preview
- Mark bill as paid/unpaid

### 4. Simple Dashboard
- List of recent bills
- Basic statistics:
  - Total bills today
  - Total amount collected
  - Number of pending payments

## Minimum Technical Requirements

### 1. Database Design
- Implement necessary tables with proper relationships
- Basic data validation

### 2. Code Quality
- Clear code organization
- Basic error handling
- Comments for complex logic

### 3. User Interface
- Clean, functional interface
- Basic form validation
- Responsive design

## Bonus Features (Optional)
- User authentication
- Role-based access control
- Advanced search/filter for patients
- Basic PDF generation for bills
- Simple search/filter for bills
- Basic input validation
- Simple audit logging

## Evaluation Criteria

### 1. Code Quality (40%)
- Clean, readable code
- Proper error handling
- Basic security considerations

### 2. Functionality (40%)
- Working core features
- Data validation
- User experience

### 3. Technical Decisions (20%)
- Database structure
- Code organization
- Feature prioritization
