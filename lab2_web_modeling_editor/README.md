# Lab 2 – Building a Full Application with the BESSER Web Modeling Editor

## 1. Introduction
In this lab, you will use the [**BESSER Web Modeling Editor**](https://editor.besser-pearl.org/) to model and generate a complete web application.

The exercise covers:

- Creating a new BESSER project
- Modeling a simple domain using a **Class Diagram**
- Defining an agent (Chatbot)
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
2. Create a new project by selecting **File → New Project** from the menu.
3. Name the project, e.g., `digital_twins_lab`, fill in the **Owner** and **Description** fields and click on **Create Project**.

When you create a new BESSER project, it automatically includes the following models:

- **Class Diagram**: Model the structure of your domain with classes and relationships.
- **Object Diagram**: Visualize example instances of your classes and their links.
- **State Machine Diagram**: Define dynamic behavior for system components.
- **Agent Diagram**: Model agents using a State Machine extension.
- **Graphical UI Editor**: Design user interfaces with a no-code, drag-and-drop editor.

These components provide a comprehensive starting point for modeling, behavior specification, and UI design in your application. Throughout this lab, you will create a class diagram, define an agent, and build a GUI to interact with your data, after generate and deploy a web app.

---

## 4. Modeling the Domain with a Class Diagram

### 4.1 Goal of the Model  
You will create a simple domain model based on a **digital twin scenario**.

A **digital twin** (DT) is a virtual copy of a real-world object, system, or process. It uses data from sensors and other sources to create a digital model that behaves like the real thing. This allows people to monitor, analyze, and test changes in the digital version before making decisions about the physical one. DTs are often used to improve performance, predict problems, and make better choices in areas like manufacturing, healthcare, and smart cities.

Our minimal DT class diagram will contain the following concepts:

- **PhysicalThing**: represents the real-world asset  
  - attributes: `name`, `location`

- **DigitalTwin**: virtual representation of the physical asset  
  - attributes: `status`, `lastSync`

- **Sensor**: a sensor attached to the physical thing  
  - attributes: `type`, `unit`

- **Measurement**: stores sensor-generated readings  
  - attributes: `timestamp`, `value`

Feel free to adapt or extend the scenario.

### 4.2 Steps

1. Open the **Class Diagram Editor** in BESSER.
2. Define the classes, attributes and relationships. For example, a **PhysicalThing** has many **Sensor**s
3. Validate the diagram by selecting the **Quality Check** menu. This option checks the syntactic correctness of the diagram. Semantic correctness (ensuring the model reflects the intended domain meaning) must still be reviewed manually, so take a moment to verify that your classes, attributes, and relationships accurately represent the scenario.

---

## 5. Creating an Agent with the State Machine Editor




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
