# ZeeFast

A lightweight **FastAPI-inspired web framework implementation built from scratch in Python**.

ZeeFast is an educational project created to understand how modern Python web frameworks work internally, including routing, request/response handling, middleware, dependencies, HTTP methods, query parameters, and exception handling.

> ⚠️ **This is not intended to be a production-ready replacement for FastAPI.** It is primarily a learning and experimentation project.

## 🚀 Overview

Frameworks such as FastAPI provide developers with high-level abstractions for building APIs quickly.

Instead of simply using those abstractions, this project explores how some of the underlying concepts can be implemented from scratch.

ZeeFast currently provides a basic structure for building HTTP APIs with features such as:

* API routing
* HTTP methods
* Middleware support
* Query parameter handling
* Request handling
* Response handling
* Dependency management
* HTTP status codes
* Exception handling

## 📂 Project Structure

```text
zeefast/
│
├── __pycache__/
│
├── __init__.py
├── api_router.py
├── app.py
├── depends.py
├── exceptions.py
├── request.py
├── response.py
└── status.py
```

## 🧩 Components

### `app.py`

Contains the main application implementation and acts as the entry point for creating a ZeeFast application.

### `api_router.py`

Provides routing functionality for defining API endpoints and organizing routes.

The router supports common HTTP methods such as:

* `GET`
* `POST`
* `PUT`
* `PATCH`
* `DELETE`

### `request.py`

Contains the request-related functionality used to access information received from the client.

### `response.py`

Provides functionality for constructing and returning HTTP responses.

### `depends.py`

Contains the dependency-related functionality used by the framework.

This is inspired by dependency injection systems commonly found in modern Python web frameworks.

### `exceptions.py`

Contains exception handling functionality for dealing with errors that occur during request processing.

### `status.py`

Provides HTTP status codes that can be used when constructing API responses.

## ✨ Current Features

### HTTP Routing

Define API endpoints using different HTTP methods.

```text
GET
POST
PUT
PATCH
DELETE
```

### Middleware

ZeeFast includes middleware support, allowing logic to be executed during request/response processing.

Conceptually:

```text
Client Request
      ↓
  Middleware
      ↓
   Router
      ↓
 Endpoint
      ↓
  Response
      ↓
  Middleware
      ↓
Client Response
```

### Query Parameters

Basic query parameter handling is supported.

For example:

```text
/users?name=zeeshan
```

The framework can process query information supplied as part of the URL.

### Request & Response Handling

The framework separates request and response functionality into dedicated modules.

```text
request.py
    ↓
Request Processing
    ↓
Endpoint
    ↓
response.py
    ↓
HTTP Response
```

### Dependency System

ZeeFast includes an initial dependency mechanism inspired by dependency injection systems used in frameworks such as FastAPI.

## 🎯 Why I Built This

The purpose of ZeeFast is to understand what happens **under the hood of a Python web framework**.

Rather than only learning how to use FastAPI, this project explores concepts such as:

* HTTP request processing
* URL routing
* API endpoint registration
* Middleware execution
* Query parameter parsing
* Request/response abstraction
* Dependency injection
* Exception handling
* HTTP status codes
* Framework architecture

The project follows a similar learning philosophy to:

```text
Using a Framework
       ↓
Understanding the Framework
       ↓
Implementing Framework Concepts
       ↓
Building Better Applications
```

## 🛠️ Technologies

* **Python**
* **HTTP**
* **Web APIs**
* **Object-Oriented Programming**
* **Web Framework Architecture**

## 📈 Project Status

ZeeFast is an **experimental/educational project** and is still under development.

Current functionality includes:

* [x] Application structure
* [x] API Router
* [x] GET routes
* [x] POST routes
* [x] PUT routes
* [x] PATCH routes
* [x] DELETE routes
* [x] Request handling
* [x] Response handling
* [x] Middleware support
* [x] Query parameter handling
* [x] Dependency system
* [x] Exception handling
* [x] HTTP status codes

Possible future improvements:

* [ ] Path parameters
* [ ] Request body parsing
* [ ] JSON validation
* [ ] Pydantic-style schemas
* [ ] Async endpoint support
* [ ] Better dependency injection
* [ ] OpenAPI/Swagger documentation
* [ ] Authentication utilities
* [ ] More comprehensive exception handling
* [ ] Automated tests
* [ ] Performance improvements

## 📚 Inspiration

ZeeFast is inspired by the architecture and developer experience of modern Python API frameworks, particularly the ideas behind **FastAPI**.

The purpose is not to reproduce FastAPI, but to learn how the concepts behind frameworks like it can be designed and implemented.

## ⚠️ Disclaimer

ZeeFast is a **learning project**.

It has not been designed, tested, or optimized for production workloads. For real-world applications, use established and production-tested frameworks such as FastAPI, Django, or Flask.

## 👨‍💻 Author

**Zeeshan Aftab**

Built as a hands-on project to explore **Python web framework internals and API development**.

---

⭐ If you're also interested in understanding how web frameworks work internally, feel free to explore the code and experiment with it.
