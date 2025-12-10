# Week 11: Object-Oriented Architecture & AI Integration
Student Name: Ali Layan Thohir
Student ID: M01091333
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
This iteration represents a major refactoring of the platform into a robust Object-Oriented (OOP) architecture. It separates concerns using the Model-View-Service pattern and introduces an AI-powered assistant. The codebase is modularized to improve scalability, maintainability, and security.

## Features
- **OOP Refactoring**: Transformation of functional code into structured Classes and Objects.
- **AI Assistant**: Integration of OpenAI API to provide role-specific expert advice (e.g., analyzing threats for Security Analysts or debugging for IT Admins).
- **Service Layer**: Dedicated managers for Authentication, Database handling, and AI services.
- **Data Models**: Class-based representations of Users, Tickets, Incidents, and Datasets.
- **Advanced Navigation**: Dynamic sidebar with logout functionality and role-specific module loading.

## Technical Implementation
- **Architecture**: Modular design separating Models (`models/`), Services (`services/`), and Views (`pages/`).
- **Classes**:
    - **Models**: `User`, `SecurityIncident`, `Dataset`, `ITTicket`.
    - **Services**: `DatabaseManager`, `AuthManager`, `AIAssistant`.
- **AI Integration**:
    - **API**: OpenAI (`gpt-4o`).
    - **Context**: Role-based system prompts (Cybersecurity, Data Science, IT).
- **Database**: SQLite (`intelligence_platform.db`) accessed via the `DatabaseManager` class.
- **Modules**:
    - `bcrypt`: Secure password hashing.
    - `openai`: AI chat completion.
    - `pandas`: Data manipulation for dashboards.
    - `streamlit`: Web interface rendering.