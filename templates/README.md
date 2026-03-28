# Tea Vending ERP - Frontend Templates

This folder contains HTML/Jinja2 templates for the Tea Vending ERP web application.

## Template Structure

```
templates/
├── base.html              # Base template with header, sidebar, footer
├── index.html             # Login page
├── dashboard.html         # Main dashboard
├── leads_list.html        # View all leads
├── leads_add.html         # Add new lead form
├── leads_schedule_demo.html # Schedule demo for leads
├── clients_list.html      # View all clients
├── clients_add.html       # Convert lead to client
├── work_orders_list.html  # View all work orders
├── work_orders_add.html   # Add new work order
├── machines_list.html     # View all machines
└── machines_add.html      # Add new machine
```

## Features

- **Responsive Design**: Uses Bootstrap 5 for mobile-friendly layouts
- **Authentication**: Integrated with existing login API using JWT tokens
- **Modular Structure**: Base template with reusable components
- **API Integration**: JavaScript functions for CRUD operations
- **Navigation**: Sidebar navigation with active states

## Authentication Flow

1. User logs in via `index.html` (login page)
2. JWT token stored in localStorage
3. All API calls include `Authorization: Bearer <token>` header
4. Automatic redirect to login on 401 responses

## API Endpoints Used

### Authentication
- `POST /users/login` - User login

### Leads
- `GET /leads/all-leads` - Get all leads
- `POST /leads/create-leads` - Create new lead
- `DELETE /leads/{id}` - Delete lead
- `POST /leads/{id}/schedule-demo` - Schedule demo

### Clients
- `GET /clients/` - Get all clients
- `POST /clients/convert/{lead_id}` - Convert lead to client

### Work Orders
- `GET /work-orders/` - Get all work orders
- `POST /work-orders/` - Create work order
- `DELETE /work-orders/{id}` - Delete work order

### Machines
- `GET /machines/` - Get all machines
- `POST /machines/add-machines` - Create machine
- `DELETE /machines/{id}` - Delete machine

### Users
- `GET /users/all` - Get all users (for dropdowns)

## Backend Route Integration

Add these routes to your `main.py`:

```python
# Additional template routes
@app.get("/leads", response_class=HTMLResponse)
def leads(request: Request):
    return templates.TemplateResponse("leads_list.html", {"request": request})

@app.get("/leads/add", response_class=HTMLResponse)
def leads_add(request: Request):
    return templates.TemplateResponse("leads_add.html", {"request": request})

@app.get("/leads/schedule", response_class=HTMLResponse)
def leads_schedule(request: Request):
    return templates.TemplateResponse("leads_schedule_demo.html", {"request": request})

@app.get("/clients", response_class=HTMLResponse)
def clients(request: Request):
    return templates.TemplateResponse("clients_list.html", {"request": request})

@app.get("/clients/add", response_class=HTMLResponse)
def clients_add(request: Request):
    return templates.TemplateResponse("clients_add.html", {"request": request})

@app.get("/work-orders", response_class=HTMLResponse)
def work_orders(request: Request):
    return templates.TemplateResponse("work_orders_list.html", {"request": request})

@app.get("/work-orders/add", response_class=HTMLResponse)
def work_orders_add(request: Request):
    return templates.TemplateResponse("work_orders_add.html", {"request": request})

@app.get("/machines", response_class=HTMLResponse)
def machines(request: Request):
    return templates.TemplateResponse("machines_list.html", {"request": request})

@app.get("/machines/add", response_class=HTMLResponse)
def machines_add(request: Request):
    return templates.TemplateResponse("machines_add.html", {"request": request})
```

## Styling

- Uses Bootstrap 5.1.3 for responsive design
- Font Awesome 6.0.0 for icons
- Custom CSS for sidebar and authentication styling
- Professional color scheme with gradients

## JavaScript Features

- Form validation
- Loading states during API calls
- Error handling with user-friendly messages
- Automatic authentication checks
- Dynamic table population
- Modal-like interactions (alerts for now)

## Security Notes

- JWT tokens stored in localStorage (consider httpOnly cookies for production)
- All API calls include authentication headers
- Automatic logout on authentication failures
- Input validation on forms

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Progressive enhancement approach

## Development Notes

- Templates use Jinja2 syntax for server-side rendering
- JavaScript is vanilla (no frameworks) for simplicity
- API calls use Fetch API
- Error handling is basic - enhance for production use