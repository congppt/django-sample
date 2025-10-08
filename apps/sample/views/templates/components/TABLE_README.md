# Advanced Table Component

A comprehensive, responsive table component for Django with pagination, filtering, sorting, and action buttons.

## Features

- ✅ **Responsive Design** - Works on all screen sizes
- ✅ **Dynamic Pagination** - Configurable page sizes (10, 25, 50, 100)
- ✅ **Real-time Search** - Instant filtering as you type
- ✅ **Custom Filters** - Dropdown filters for specific columns
- ✅ **Column Sorting** - Click headers to sort data
- ✅ **Action Buttons** - Header actions and row-specific actions
- ✅ **Multiple Data Types** - Support for text, badges, dates, currency, booleans, images
- ✅ **Empty State** - Beautiful empty state when no data is found
- ✅ **Loading States** - Built-in loading animations
- ✅ **Accessibility** - ARIA labels and keyboard navigation

## Usage

### 1. Basic Usage

```html
{% include 'templates/components/table.html' with table_title="My Data" table_columns=columns table_data=data %}
```

### 2. Full Configuration

```html
{% include 'templates/components/table.html' with 
    table_title="User Management" 
    table_description="Manage users, roles, and permissions"
    table_columns=table_columns 
    table_data=table_data 
    table_actions=table_actions 
    table_row_actions=table_row_actions 
    table_filters=table_filters 
%}
```

## Configuration

### Table Columns

Define your table columns with the following structure:

```python
table_columns = [
    {
        'name': 'id',           # Field name in your data
        'label': 'ID',          # Display label
        'type': 'number',       # Data type (text, number, currency, date, datetime, boolean, badge, image)
        'sortable': True        # Enable/disable sorting
    },
    {
        'name': 'name',
        'label': 'Full Name',
        'type': 'text',
        'sortable': True
    },
    {
        'name': 'status',
        'label': 'Status',
        'type': 'badge',
        'sortable': True
    },
    {
        'name': 'salary',
        'label': 'Salary',
        'type': 'currency',
        'sortable': True
    },
    {
        'name': 'created_at',
        'label': 'Created',
        'type': 'datetime',
        'sortable': True
    },
    {
        'name': 'is_active',
        'label': 'Active',
        'type': 'boolean',
        'sortable': True
    }
]
```

### Data Types

- **text** - Plain text
- **number** - Numeric values with formatting
- **currency** - Currency formatting with $ symbol
- **date** - Date formatting (M d, Y)
- **datetime** - Date and time formatting (M d, Y H:i)
- **boolean** - Check/cross icons
- **badge** - Colored badges with automatic color mapping
- **image** - Profile images with rounded styling

### Table Actions (Header Buttons)

```python
table_actions = [
    {
        'label': 'Add User',
        'icon': 'plus.svg',        # Icon from your static/icons folder
        'color': 'blue',           # Tailwind color (blue, green, red, yellow, etc.)
        'onclick': 'addUser()',    # JavaScript function to call
        'disabled': False          # Optional: disable the button
    },
    {
        'label': 'Export Data',
        'icon': 'export.svg',
        'color': 'green',
        'onclick': 'exportData()'
    }
]
```

### Row Actions (Per-row Buttons)

```python
table_row_actions = [
    {
        'label': 'View',
        'icon': 'eye.svg',
        'color': 'blue',
        'onclick': 'viewUser(this)'
    },
    {
        'label': 'Edit',
        'icon': 'edit.svg',
        'color': 'yellow',
        'onclick': 'editUser(this)'
    },
    {
        'label': 'Delete',
        'icon': 'close.svg',
        'color': 'red',
        'onclick': 'deleteUser(this)'
    }
]
```

### Custom Filters

```python
table_filters = [
    {
        'name': 'status',          # Field name to filter
        'label': 'Status',         # Display label
        'options': [               # Filter options
            {'value': 'Active', 'label': 'Active'},
            {'value': 'Inactive', 'label': 'Inactive'},
            {'value': 'Pending', 'label': 'Pending'}
        ]
    },
    {
        'name': 'department',
        'label': 'Department',
        'options': [
            {'value': 'Engineering', 'label': 'Engineering'},
            {'value': 'Marketing', 'label': 'Marketing'},
            {'value': 'Sales', 'label': 'Sales'}
        ]
    }
]
```

## JavaScript API

The table component provides several JavaScript functions for customization:

### Global Functions

- `filterTable()` - Trigger table filtering
- `sortTable(columnIndex)` - Sort by column index
- `changePageSize()` - Change page size
- `changePage(direction)` - Navigate pages ('prev', 'next', or page number)

### Event Handling

```javascript
// Handle row action clicks
document.addEventListener('click', function(e) {
    if (e.target.closest('[data-action="edit"]')) {
        const row = e.target.closest('tr');
        const userId = row.dataset.userId;
        // Your edit logic here
    }
});

// Custom search functionality
function customSearch() {
    const searchTerm = document.getElementById('table-search').value;
    // Your custom search logic
    filterTable();
}
```

## Styling

The component uses Tailwind CSS classes and includes custom CSS for:

- Smooth hover transitions
- Custom scrollbars
- Loading animations
- Responsive adjustments

### Custom Colors

Badge colors are automatically mapped based on values:

```python
# In templatetags/table_filters.py
color_map = {
    'Active': 'green',
    'Inactive': 'red',
    'Pending': 'yellow',
    'Admin': 'purple',
    'Manager': 'blue',
    'User': 'gray',
    # Add your own mappings
}
```

## Server-side Integration

For large datasets, you can implement server-side pagination, filtering, and sorting:

```python
def table_ajax_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 25))
    search = request.GET.get('search', '')
    
    # Query your database
    queryset = MyModel.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )
    
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    return JsonResponse({
        'data': list(page_obj.object_list.values()),
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
        }
    })
```

## Example Implementation

See `example_table_view.py` for a complete implementation example with sample data and all features configured.

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Dependencies

- Tailwind CSS (included via CDN in base template)
- Django template system
- Modern JavaScript (ES6+)

## Customization

The component is highly customizable through:

1. **Template variables** - Pass different configurations
2. **CSS classes** - Override Tailwind classes
3. **JavaScript functions** - Add custom event handlers
4. **Template filters** - Create custom data formatters
5. **Server-side logic** - Implement custom filtering/sorting

## Performance Tips

1. Use server-side pagination for large datasets (>1000 rows)
2. Implement database-level filtering for better performance
3. Use `select_related()` and `prefetch_related()` for related data
4. Consider caching for frequently accessed data
5. Use lazy loading for images in table cells
