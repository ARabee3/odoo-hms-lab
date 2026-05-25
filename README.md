# Hospital Management System (HMS) - Odoo Module

A custom Odoo 19 module built as part of lab assignments for managing hospital patients, departments, doctors, and CRM customer integration.

## Odoo Version

**19.0**

## Features

### Lab 02 - Core Module

- **Departments** (`hms.department`)
  - Name, capacity, and open/closed status
  - View patients assigned to each department

- **Doctors** (`hms.doctors`)
  - First name, last name, and profile image

- **Patients** (`hms.patient`)
  - Personal details: name, birth date, age, blood type, address
  - Medical info: PCR status, CR ratio, history
  - Link to a department and multiple doctors
  - **State tracking**: Undetermined, Good, Fair, Serious
  - **Auto-generated log history** on every state change

- **Business Rules**
  - Closed departments cannot be selected
  - Doctors field is read-only until a department is chosen
  - CR ratio becomes mandatory when PCR is checked
  - History field is hidden for patients under 50
  - PCR is auto-checked for patients under 30 with a warning

### Lab 03 - CRM Integration & Enhancements

- **Patient Email**
  - Valid email format validation
  - Unique email constraint across all patients

- **Auto-Calculated Age**
  - Age is computed automatically from birth date

- **CRM Customer Link**
  - Added `related_patient_id` field on `res.partner` (Customers)
  - Field visible in the **Misc** group of the **Sales & Purchase** tab

- **Customer Constraints**
  - Prevent linking a customer to a patient if the customer's email already exists in patient records
  - Prevent deleting customers that are linked to patients

- **Customer Views**
  - Show **Website** field in customer list view
  - Make **Tax ID (VAT)** field mandatory for customers

### Lab 04 - Security & Reporting

- **Security Groups**
  - **User**: Can create/read/update own patients only; read-only access to departments and doctors; cannot see doctor field or Doctors menu
  - **Manager**: Full CRUD on patients, departments, doctors; can see doctor field and Doctors menu

- **Record Rules**
  - Users can only see their own patient records
  - Managers can see all patient records

- **Patient Status Report**
  - QWeb PDF report matching the lab design
  - Red title, patient image, two-column info layout
  - Log History table with blue header
  - Print button on patient form

## Installation

1. Copy this module folder into your Odoo `addons` path (or any folder in `addons_path`).
2. Restart the Odoo server.
3. Enable **Developer Mode**.
4. Go to **Apps → Update Apps List**.
5. Search for "Hospital Management System" and click **Install**.
6. Assign users to either the **User** or **Manager** group under Settings → Users.

## Models

| Model | Description |
|-------|-------------|
| `hms.patient` | Patient records with medical info |
| `hms.department` | Hospital departments |
| `hms.doctors` | Doctor records |
| `hms.patient.log` | Audit log for patient state changes |

## Views

- Form and list views for Patients, Departments, and Doctors
- Status bar for patient state selection
- Many2many tags widget for doctor selection
- Conditional visibility and readonly attributes
- Inherited customer form with `related_patient_id`
- Inherited customer list with `website`
- QWeb PDF report for patient status

## Security

| Group | Patients | Departments | Doctors | Doctor Field | Doctor Menu |
|-------|----------|-------------|---------|--------------|-------------|
| User | Own records only | Read only | Read only | Hidden | Hidden |
| Manager | All CRUD | All CRUD | All CRUD | Visible | Visible |

## License

This is an educational project. See Odoo's [LICENSE](https://github.com/odoo/odoo/blob/19.0/LICENSE) for the framework.
