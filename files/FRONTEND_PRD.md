# Frontend PRD: Moodboard — Shop the Aesthetic, Not the Item

## Overview

**Product Name:** Moodboard

**One-liner:** Upload inspo images + a prompt, get shoppable products that match the *feeling*, not the pixels.

**Problem:** Users find aesthetic inspiration everywhere (Pinterest, movies, Instagram, real life) but have no way to translate "this mood" into actual purchasable items. Existing visual search tools find identical or similar-looking items — they don't understand aesthetic energy.

**Solution:** A web app that uses vision AI to extract the mood, color palette, textures, and style energy from uploaded images, then returns shoppable products that capture that aesthetic.

---

## User Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     LANDING PAGE                            │
│                                                             │
│   "Shop the mood, not the item"                            │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                                                     │  │
│   │         Drag & drop images or click to upload       │  │
│   │                    (1-5 images)                     │  │
│   │                                                     │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ Describe what you want (optional)                   │  │
│   │ e.g., "This vibe but for summer" or "Under $100"   │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│              [ Shop This Mood ] (primary CTA)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     LOADING STATE                           │
│                                                             │
│              Analyzing your mood...                         │
│              [progress indicator]                           │
│                                                             │
│   Show uploaded images as thumbnails                        │
│   Subtle animation (color extraction visual?)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     RESULTS PAGE                            │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  YOUR MOOD: "Quiet Luxury Coastal"                  │  │
│   │                                                     │  │
│   │  [cream] [camel] [white] [soft grey] (color dots)  │  │
│   │                                                     │  │
│   │  Mood: Effortless, polished, understated           │  │
│   │  Key pieces: Oversized blazer, linen pants...      │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  Refine: [More casual] [Higher budget] [Add shoes] │  │
│   │          [Different colors] [Custom: ____]         │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│   │ Product │ │ Product │ │ Product │ │ Product │        │
│   │  Image  │ │  Image  │ │  Image  │ │  Image  │        │
│   │         │ │         │ │         │ │         │        │
│   │ Name    │ │ Name    │ │ Name    │ │ Name    │        │
│   │ $XX     │ │ $XX     │ │ $XX     │ │ $XX     │        │
│   │ [Shop]  │ │ [Shop]  │ │ [Shop]  │ │ [Shop]  │        │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
│                                                             │
│   (12-20 products in responsive grid)                      │
│                                                             │
│   [ Start Over ] (secondary CTA)                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Pages & Components

### Page 1: Home / Upload Page

**Route:** `/`

**Purpose:** User uploads images and enters optional prompt

**Components:**

#### 1.1 Header
- Logo/wordmark: "Moodboard" (top left)
- Tagline: "Shop the vibe, not the item"
- Simple, minimal — don't distract from the upload area

#### 1.2 Image Upload Zone
- Drag & drop area (primary interaction)
- Click to open file picker (secondary)
- Accepts: JPG, PNG, WEBP
- Limit: 1-5 images
- Max file size: 5MB per image
- Show thumbnails of uploaded images below/inside the zone
- Each thumbnail has an X to remove
- Show count: "3/5 images"

**States:**
- Empty: Dashed border, upload icon, "Drag & drop images or click to upload"
- Hovering with file: Border highlights, "Drop to upload"
- Has images: Show thumbnail grid, "Add more" button if under 5
- Error: Red border, "File too large" or "Unsupported format"

#### 1.3 Prompt Input
- Single-line text input (expands if needed)
- Placeholder: `Describe what you want (optional) — e.g., "This vibe but for summer"`
- Character limit: 200 characters
- Show character count when typing

#### 1.4 Submit Button
- Text: "Shop This Mood"
- Disabled until at least 1 image uploaded
- Full width on mobile, centered on desktop
- Loading state: "Analyzing..." with spinner

#### 1.5 Example Prompts (Optional Enhancement)
- Below the prompt input
- Clickable chips: "But affordable" / "For summer" / "Date night" / "Work appropriate"
- Clicking a chip appends it to the prompt input

---

### Page 2: Results Page

**Route:** `/results` (or keep as single-page app with state change)

**Purpose:** Display vibe analysis and shoppable products

**Components:**

#### 2.1 Vibe Summary Card
- **Vibe Name:** Large, bold text (e.g., "Quiet Luxury Coastal")
- **Color Palette:** 4-6 circular color swatches with hex codes on hover
- **Mood:** 2-3 descriptive words
- **Key Pieces:** Comma-separated list of 5-7 items
- **Avoid:** (Optional) What doesn't fit this vibe
- Collapsible on mobile to save space

#### 2.2 Uploaded Images Preview
- Small thumbnails of what the user uploaded
- Collapsed by default, expandable
- "Based on your images" label

#### 2.3 Refinement Bar
- Horizontal scrollable row of filter chips
- Quick filters: "More casual" / "More dressy" / "Lower budget" / "Higher budget" / "Add accessories" / "Add shoes"
- Custom refinement: Text input that reopens with the original images + new prompt
- Clicking a refinement triggers a new API call

#### 2.4 Product Grid
- Responsive grid: 2 columns mobile, 3 columns tablet, 4 columns desktop
- 12-20 products initially
- "Load more" button if more results available

#### 2.5 Product Card
- **Image:** Square aspect ratio, object-fit cover
- **Sale Badge:** If `on_sale: true`, show red "SALE" badge in corner
- **Brand:** Small text above product name (e.g., "Vince")
- **Product Name:** Max 2 lines, truncate with ellipsis
- **Price:** Bold, prominent. If on sale, show original price with strikethrough
- **Retailer:** Small text below price (e.g., "from Nordstrom")
- **Shop Button:** "Shop" or "View" — opens product URL in new tab (this is an affiliate link!)
- **Out of Stock:** If `in_stock: false`, grey out card and show "Out of Stock"
- Hover state: Subtle lift/shadow
- Clicking anywhere on card opens product link

#### 2.6 Empty State
- If no products found: "We couldn't find products matching this vibe. Try uploading different images or adjusting your prompt."
- Show "Start Over" button

#### 2.7 Start Over Button
- Secondary button style
- Returns to home page with cleared state

---

## Technical Specifications

### Tech Stack
- **Framework:** React (Create React App or Next.js)
- **Styling:** Tailwind CSS
- **State Management:** React useState/useContext (keep it simple)
- **HTTP Client:** Fetch API or Axios
- **Image Handling:** Browser FileReader API for previews

### API Integration

#### Endpoint: `POST /api/vibecheck`

**Request:**
```javascript
{
  "images": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRg...", // Base64 encoded
    "data:image/png;base64,iVBORw0KGgo..."
  ],
  "prompt": "This vibe but for summer" // Optional, can be empty string
}
```

**Response:**
```javascript
{
  "success": true,
  "vibe": {
    "name": "Quiet Luxury Coastal",
    "mood": "Effortless, polished, understated confidence",
    "color_palette": [
      {"name": "Cream", "hex": "#F5F5DC"},
      {"name": "Camel", "hex": "#C19A6B"},
      {"name": "White", "hex": "#FFFFFF"},
      {"name": "Soft Grey", "hex": "#D3D3D3"}
    ],
    "textures": ["linen", "cashmere", "cotton", "silk"],
    "key_pieces": [
      "Oversized neutral blazer",
      "White tank bodysuit",
      "High-waisted tailored trousers",
      "Minimal gold jewelry",
      "Clean white sneakers"
    ],
    "avoid": ["Loud logos", "neon colors", "distressed denim"]
  },
  "products": [
    {
      "id": "ss_123",
      "name": "Oversized Linen Blazer",
      "brand": "Vince",
      "price": 89.99,
      "original_price": 145.00,
      "on_sale": true,
      "currency": "USD",
      "image_url": "https://img.shopstyle-cdn.com/...",
      "product_url": "https://api.shopstyle.com/action/apiVisitRetailer?id=...",
      "retailer": "Nordstrom",
      "category": "Jackets",
      "match_reason": "Oversized neutral blazer",
      "in_stock": true
    },
    // ... more products
  ]
}
```

**Error Response:**
```javascript
{
  "success": false,
  "error": "Unable to analyze images. Please try again."
}
```

### Image Handling

**Upload Process:**
1. User selects/drops files
2. Validate file type (JPG, PNG, WEBP only)
3. Validate file size (< 5MB each)
4. Generate preview URL using `URL.createObjectURL()`
5. On submit, convert each image to Base64 using FileReader
6. Send Base64 strings to backend

**Code Example:**
```javascript
const convertToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

const handleSubmit = async () => {
  const base64Images = await Promise.all(
    images.map(file => convertToBase64(file))
  );
  
  const response = await fetch('/api/vibecheck', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      images: base64Images,
      prompt: userPrompt
    })
  });
  
  const data = await response.json();
  // Handle response
};
```

---

## UI/UX Requirements

### Visual Design

**Overall Aesthetic:**
- Clean, minimal, lots of whitespace
- Let the user's images and product results be the visual focus
- Neutral base colors with subtle accent

**Color Palette:**
- Background: #FAFAFA (off-white)
- Text: #1A1A1A (near-black)
- Accent: #000000 (black) for buttons
- Secondary: #6B7280 (grey) for secondary text
- Error: #EF4444 (red)
- Success: #10B981 (green)

**Typography:**
- Headings: Inter or SF Pro Display, semibold
- Body: Inter or SF Pro Text, regular
- Vibe Name: Large (32-40px), bold, can be slightly stylized

**Spacing:**
- Use 8px grid system
- Generous padding on containers (24-48px)
- Card gap: 16px mobile, 24px desktop

### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Accessibility
- All images have alt text
- Color contrast meets WCAG AA
- Keyboard navigable
- Focus states visible
- Loading states announced to screen readers

---

## States & Error Handling

### Loading States
1. **Image uploading:** Show progress bar per image
2. **Analyzing vibe:** Full-screen or modal overlay with animation
   - "Analyzing your mood..."
   - Show uploaded thumbnails
   - Subtle animation (optional: color dots floating)
   - Estimated time: 5-15 seconds

### Error States
1. **Invalid file type:** "Please upload JPG, PNG, or WEBP images"
2. **File too large:** "Image must be under 5MB"
3. **Too many images:** "Maximum 5 images allowed"
4. **API error:** "Something went wrong. Please try again."
5. **No products found:** "We couldn't find products for this vibe. Try different images."

### Empty States
1. **No images uploaded:** Show upload prompt with examples
2. **No results:** Friendly message with suggestions

---

## Future Enhancements (Post-MVP)

1. **Save vibes:** User accounts to save favorite vibes
2. **Share vibe:** Shareable link to results page
3. **Price filter:** Slider to set budget range
4. **Category filter:** Tops, bottoms, shoes, accessories
5. **Retailer filter:** Only show results from preferred stores
6. **Image URL input:** Paste a URL instead of uploading
7. **Browser extension:** Right-click any image → "Shop this vibe"
8. **Mobile app:** Native iOS/Android with camera integration

---

## Success Metrics

1. **Upload completion rate:** % of users who upload at least 1 image
2. **Search completion rate:** % of uploads that result in clicking "Shop This Mood"
3. **Product click-through rate:** % of users who click at least 1 product
4. **Refinement usage:** % of users who use refinement filters
5. **Return rate:** % of users who come back within 7 days

---

## File Structure

```
src/
├── components/
│   ├── Header.jsx
│   ├── ImageUploader.jsx
│   ├── PromptInput.jsx
│   ├── SubmitButton.jsx
│   ├── LoadingOverlay.jsx
│   ├── VibeSummary.jsx
│   ├── ColorPalette.jsx
│   ├── RefinementBar.jsx
│   ├── ProductGrid.jsx
│   ├── ProductCard.jsx
│   └── ErrorMessage.jsx
├── pages/
│   ├── Home.jsx
│   └── Results.jsx (or use state in single page)
├── hooks/
│   ├── useImageUpload.js
│   └── useVibeCheck.js
├── utils/
│   ├── imageUtils.js (base64 conversion, validation)
│   └── api.js (API calls)
├── styles/
│   └── globals.css (Tailwind imports)
├── App.jsx
└── index.js
```

---

## Development Phases

### Phase 1: Core Upload (2-3 hours)
- [ ] Set up React project with Tailwind
- [ ] Build ImageUploader component with drag & drop
- [ ] Add image preview thumbnails
- [ ] Add prompt input
- [ ] Basic layout and styling

### Phase 2: API Integration (1-2 hours)
- [ ] Connect to backend `/api/vibecheck` endpoint
- [ ] Handle loading states
- [ ] Handle error states
- [ ] Parse and store response

### Phase 3: Results Display (2-3 hours)
- [ ] Build VibeSummary component
- [ ] Build ProductGrid and ProductCard
- [ ] Responsive layout
- [ ] "Start Over" flow

### Phase 4: Polish (1-2 hours)
- [ ] Loading animation
- [ ] Refinement filters (basic)
- [ ] Error handling edge cases
- [ ] Mobile testing
- [ ] Final styling pass
