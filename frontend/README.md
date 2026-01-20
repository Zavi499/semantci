# Semantic Keyword Analyzer - Frontend

A modern, interactive web interface for the Semantic Keyword Analysis Tool.

## Features

- **Single Keyword Analysis**: Analyze individual keywords with detailed insights
- **Batch Processing**: Analyze multiple keywords simultaneously
- **Interactive Visualizations**: Knowledge graph visualization with vis.js
- **Real-time Results**: Instant analysis with loading states
- **Analysis History**: Track and revisit previous analyses
- **Export Functionality**: Download results as JSON
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Cache Management**: Monitor and clear API cache

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No framework dependencies
- **Vis.js**: Network/graph visualization
- **Font Awesome**: Icon library
- **LocalStorage**: Client-side history persistence

## Getting Started

### Prerequisites

- The backend API must be running on `http://localhost:8000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Running the Frontend

#### Option 1: Through FastAPI (Recommended)

The frontend is automatically served by the FastAPI backend:

```bash
# Start the API server (from project root)
python -m uvicorn api.main:app --reload

# Open browser to:
http://localhost:8000
```

The frontend will be automatically loaded!

#### Option 2: Direct File Access

Simply open the `index.html` file in your browser:

```bash
# From the frontend directory
open index.html
# or
firefox index.html
# or
google-chrome index.html
```

**Note**: Make sure the API is still running at `http://localhost:8000` for full functionality.

#### Option 3: Local HTTP Server

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8080

# Open browser to:
http://localhost:8080
```

## Usage Guide

### Single Keyword Analysis

1. Navigate to the **Analyze** tab (default)
2. Enter a keyword in the search box
3. Click **Analyze** or press Enter
4. View comprehensive analysis results:
   - Entity information and classification
   - Salience and authority scores
   - Semantic relevance and topic clusters
   - Knowledge graph visualization
   - Taxonomy and ontology
   - Schema.org markup

### Batch Analysis

1. Click the **Batch** tab
2. Enter keywords (one per line)
3. Choose parallel processing option
4. Click **Analyze Batch**
5. View summary statistics
6. Click individual results for detailed view

### Analysis History

1. Click the **History** tab
2. View all previous analyses
3. Click any history item to view full results
4. History is automatically saved in browser storage

### Quick Examples

Click any of the example keywords to instantly analyze:
- Python
- React
- ML (Machine Learning)
- Docker
- SEO

## Features Breakdown

### Overview Section
- Core entity identification
- Entity type classification
- Primary topic
- Search intent detection

### Scoring Metrics
- **Salience** (0-100): Importance/prominence score
- **Authority** (0-100): Topical credibility score
- **Confidence** (0-100): Analysis reliability score

### Detailed Tabs

#### 1. Attributes
- Key properties and characteristics
- Descriptive features

#### 2. Semantic
- Contextual usage scenarios
- Semantically related terms
- Topic clusters and themes

#### 3. Relationships
- Entity connections
- Relationship types (is_a, part_of, etc.)

#### 4. Knowledge Graph
- Interactive network visualization
- Nodes representing entities
- Edges showing relationships
- Graph statistics (nodes, edges, density)

#### 5. Taxonomy
- Classification hierarchy
- Ontology structure
- Parent concepts

#### 6. Schema
- Schema.org structured data
- JSON-LD format
- SEO-ready markup

## API Configuration

The frontend expects the API at `http://localhost:8000`. To change this:

Edit `frontend/js/app.js`:

```javascript
const API_BASE_URL = 'http://your-api-url:port';
```

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### API Connection Failed

**Symptom**: Red offline indicator, "API Connection Error"

**Solution**:
1. Ensure backend is running: `python -m uvicorn api.main:app --reload`
2. Check API is accessible: `curl http://localhost:8000/health`
3. Verify CORS settings in `api/main.py`

### Knowledge Graph Not Rendering

**Symptom**: Empty graph visualization

**Solution**:
1. Ensure vis.js is loaded (check browser console)
2. Switch to a different tab and back to "Knowledge Graph"
3. Refresh the page

### Analysis Not Working

**Symptom**: Error messages on analysis

**Solution**:
1. Check keyword is not empty
2. Verify API is responding: Check Network tab in DevTools
3. Check browser console for JavaScript errors

### History Not Saving

**Symptom**: History disappears on refresh

**Solution**:
1. Enable LocalStorage in browser
2. Check browser privacy settings
3. Clear browser cache and try again

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── css/
│   └── style.css       # Complete styling
├── js/
│   └── app.js          # Application logic
└── README.md           # This file
```

## Key Components

### HTML Structure
- Semantic HTML5 elements
- Accessibility-friendly
- Template system for dynamic content

### CSS Architecture
- CSS Variables for theming
- Grid and Flexbox layouts
- Responsive media queries
- Smooth animations and transitions

### JavaScript Modules
- State management
- API communication
- DOM manipulation
- Event handling
- Data visualization
- LocalStorage persistence

## Customization

### Change Theme Colors

Edit CSS variables in `css/style.css`:

```css
:root {
    --primary-color: #6366f1;    /* Main brand color */
    --secondary-color: #10b981;  /* Success/accent color */
    --danger-color: #ef4444;     /* Error color */
    /* ... */
}
```

### Modify Graph Appearance

Edit graph options in `js/app.js` → `renderKnowledgeGraph()` function.

## Performance

- **Initial Load**: < 100KB total
- **API Requests**: Cached responses
- **Rendering**: Optimized DOM updates
- **Storage**: Minimal LocalStorage usage

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Advanced filtering and search
- [ ] Comparison view for multiple keywords
- [ ] Export to PDF/CSV
- [ ] Customizable visualizations
- [ ] Real-time collaboration
- [ ] API key management
- [ ] Advanced analytics dashboard

## Contributing

Found a bug or have a feature request? Please open an issue!

## License

MIT License - See main project LICENSE file

## Support

For issues specific to the frontend, check:
1. Browser console for errors
2. Network tab for API calls
3. Application → LocalStorage for history data

For API issues, see the main project README.
