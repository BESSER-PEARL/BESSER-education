# Lab 2 – Building a Full Application with the BESSER Web Modeling Editor

## 1. Introduction
In this lab, you will use the **BESSER Web Modeling Editor** to model and generate a complete web application.  
The exercise covers:

- Creating a new BESSER project
- Modeling a simple domain using a **Class Diagram**
- Defining an agent using a **State Machine**
- Creating a user interface with the **No-Code UI Editor**
- Generating and deploying the application
- Populating the database using the provided **FastAPI endpoints**
- Viewing and testing the final web application

This lab will give students hands-on experience with modeling, generation, and deployment using BESSER’s low-code capabilities.

---

## 2. Prerequisites

Before starting, ensure that you have:

- Access to the BESSER Web Modeling Editor:  
  https://editor.besser-pearl.org/
- A modern web browser (Chrome, Firefox, Edge)
- Basic understanding of class diagrams and state machines

---

## 3. Creating a New Project

1. Open the BESSER Web Modeling Editor:  
   https://editor.besser-pearl.org/
2. Click **“New Project”**
3. Name the project, e.g., `digital_twins_lab` and save it.

When you create a new BESSER project, it automatically includes the following modeling and editing tools:

- **Class Diagram**: Model the structure of your domain with classes and relationships.
- **Object Diagram**: Visualize example instances of your classes and their links.
- **State Machine Diagram**: Define dynamic behavior for system components.
- **Agent Diagram**: Model agents using a State Machine extension.
- **Graphical UI Editor**: Design user interfaces with a no-code, drag-and-drop editor.

These components provide a comprehensive starting point for modeling, behavior specification, and UI design in your application.

---

## 4. Modeling the Domain with a Class Diagram

### 4.1 Goal of the Model  
You will create a simple domain model based on a **digital twin scenario**.  
Example concepts:

- **Device**: represents a physical sensor device  
  - attributes: `id`, `name`, `location`
- **Sensor**: associated with a Device  
  - attributes: `type`, `unit`
- **Measurement**: stores sensor readings  
  - attributes: `timestamp`, `value`

Feel free to adapt or extend the scenario.

### 4.2 Steps

1. Open the **Class Diagram Editor**
2. Create the classes `Device`, `Sensor`, `Measurement`
3. Add suitable attributes to each class
4. Define relationships, for example:
   - A Device *has many* Sensors
   - A Sensor *generates many* Measurements
5. Validate the diagram

---

## 5. Creating an Agent with the State Machine Editor

### 5.1 Scenario  


### 5.2 Steps



---

## 6. Creating the User Interface with the No-Code Editor

### 6.1 Goal  
Build a basic UI to:

- List devices and sensors
- Display measurements

### 6.2 Steps

1. Open the **No-Code UI Editor**
2. Create one or more screens/pages, such as:
   - `Devices`
   - `Sensors`
   - `Measurements`
3. Drag and drop widgets:
   - Tables
   - Forms
   - Detail views
4. Bind screens to your model elements
5. Configure navigation between pages
6. Preview the UI

---

## 7. Generating and Deploying the Web Application

### 7.1 Generating the App

1. 

### 7.2 Deploying the App

1. 

---

## 8. Populating the Database Using FASTAPI

### 8.1 Using the auto-generated API

The generated backend includes auto-generated endpoints to:

- Create devices
- Register sensors
- Insert measurements

### 8.2 Steps

1. Visit `/docs` in your running FASTAPI server  
   (Swagger UI)
2. Use the **POST** endpoints to populate:
   - Devices
   - Sensors
   - Measurements
3. Verify the inserted data using the **GET** endpoints
4. Refresh the UI to confirm the data appears

---

## 9. Viewing and Testing the Application

1. Open the deployed web application in your browser
2. Navigate through the UI pages you created
3. Confirm:
   - Devices are listed
   - Sensors appear correctly
   - Measurements load
   - Agent behavior (if visible) works as expected
4. Document any issues or improvements

---

## 10. Additional Resources

- BESSER Web Modeling Editor  
  https://editor.besser-pearl.org/

- BESSER Documentation  
  https://besser.readthedocs.io/en/latest/

- BESSER GitHub Repository  
  https://github.com/BESSER-PEARL/BESSER

---
