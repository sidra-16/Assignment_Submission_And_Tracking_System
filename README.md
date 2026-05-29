# SASTS: Advanced Student Assignment Submission & Tracking System

This system moves away from traditional relational database structures to implement a high-performance, document-oriented approach for academic management. Built with MongoDB and Streamlit, it serves as a comprehensive demonstration of advanced NoSQL concepts, including hybrid data modeling, complex aggregation pipelines, and ACID-compliant transaction management.

The backend is designed using the **document model**, which allows for flexible schema evolution. By utilizing **Embedding** for high-velocity data (like grades and feedback) and **Referencing** for normalized entities (like students and departments), the system achieves an optimal balance between write-heavy performance and query efficiency.

### Gallery

|                Analytics Dashboard                |                 Aggregation Pipelines                |
| :-----------------------------------------------: | :--------------------------------------------------: |
| <img src="Screenshots/dashboard.png" width="400"> | <img src="Screenshots/aggregations.png" width="400"> |

|              Multi-Document Transactions             |              Concurrency & Locking              |
| :--------------------------------------------------: | :---------------------------------------------: |
| <img src="Screenshots/transactions.png" width="400"> | <img src="Screenshots/locking.png" width="400"> |

|                 Database Views                |           Query Indexing & Optimization          |
| :-------------------------------------------: | :----------------------------------------------: |
| <img src="Screenshots/views.png" width="400"> | <img src="Screenshots/indexing.png" width="400"> |

### Advanced Database Features

The application implements several critical database management strategies to handle large-scale academic data:

* **Hybrid Data Modeling**: Optimizes storage by embedding frequently accessed sub-documents and referencing shared entities across collections.
* **Multi-Stage Aggregations**: Implements complex data processing pipelines for real-time analytics, including joins ($lookup) and data reshaping ($unwind, $project).
* **ACID Transactions**: Ensures multi-document consistency during submission workflows, preventing partial data writes in the event of system failures.
* **Concurrency Control**: Demonstrates both Optimistic and Pessimistic locking mechanisms to manage simultaneous data access without race conditions.
* **Virtual Collections (Views)**: Provides abstracted, read-only "virtual tables" for complex summaries like active student lists and submission metrics.
* **Index Optimization**: Utilizes compound and single-field indexing to transform full collection scans into targeted index seeks.

### Project Structure

```text
.
├── app.py
├── db.py
├── styles.py
├── generate_data.py
├── .streamlit/
│   └── config.toml
├── .gitattributes
├── assignments.json
├── courses.json
├── departments.json
├── instructors.json
├── notifications.json
├── students.json
├── submission.json
└── submissions.json
```

### Setup and Installation

This project requires MongoDB Community Server installed and running on your local machine.

#### Clone the repository

```bash
git clone https://github.com/yourusername/sasts-mongodb.git
cd sasts-mongodb
```

#### Install the required Python libraries

```bash
pip install streamlit pymongo pandas
```

#### Initialize the Database

Ensure MongoDB is running on `localhost:27017`, then execute the data generation script to seed the collections:

```bash
python generate_data.py
```

#### Launch the System

```bash
streamlit run app.py
```

### Technologies and References

* **[MongoDB](https://www.mongodb.com/)**: The core NoSQL document database used for all storage.
* **[PyMongo](https://pymongo.readthedocs.io/)**: The official Python driver used for high-level database operations and transactions.
* **[Streamlit](https://docs.streamlit.io/)**: The framework used for building the real-time data management dashboard.
* **[ACID Transactions](https://www.mongodb.com/docs/manual/core/transactions/)**: Used to maintain database consistency and reliability during multi-document operations.
