# Time-Money Trade-Off Calculator - Enriched Specification

## Overview

A tool to help high-earning households calculate their effective hourly rate and make informed decisions about outsourcing tasks vs. doing them themselves.

**Target Users**: SF-based, high-income dual-earner households (tech + professional backgrounds)

**Core Question**: "What is my time actually worth, and should I hire someone to do this task?"

**File**: `time-money-calculator.html`

---

## Decisions Made

| Topic | Decision | Rationale |
|-------|----------|-----------|
| Income mode | Either/or toggle (single vs dual-earner) | Flexibility for different household types |
| Tax rate | Editable with 20% default | Power users can adjust, but reasonable default |
| Market rates | Show outsourcing costs alongside time cost | Helps decision-making with direct comparison |
| Pricing region | User-selectable dropdown | Different metros have very different costs |
| Task categories | Household + Personal errands + Childcare | Most relevant for target audience |
| Custom tasks | No - fixed list only | Simpler UX |
| Calculation | Real-time updates | Responsive feel, no button needed |
| Recommendations | Subtle hints (color-coding) | Let users draw conclusions, don't be preachy |
| Philosophy text | Brief intro + personal disclaimer | Acknowledge this is hard to conceptualize |
| Region defaults | Pre-fill median income per region | Reduces friction, gives useful starting point |
| Dual-earner display | Show both rates separately | Simple, no complex "who should do it" logic |
| Childcare tasks | Always visible | Simpler, users ignore if not applicable |
| Citations | No formal citations | Expandable section to edit assumptions instead |
| Validation | Allow any values | Trust users, just calculate |

---

## Inputs

### Primary Inputs

1. **Region Selector** (dropdown)
   - SF Bay Area (default)
   - New York City
   - Los Angeles
   - Seattle
   - Boston
   - Each region sets default values for income AND outsourcing costs

2. **Income Mode Toggle**
   - Single earner mode: One income field
   - Dual earner mode: Two income fields (Person A, Person B)

3. **Annual Income**
   - Single mode: One field, pre-filled with region median
   - Dual mode: Two fields, each pre-filled with region median / 2
   - Currency input with formatting

4. **Hours Worked Per Week**
   - Default: 45 hours
   - Single number field

5. **Weeks Worked Per Year**
   - Default: 50 weeks (accounts for vacation/holidays)
   - Single number field

6. **Tax Rate**
   - Default: 20%
   - Editable input
   - Small helper text: "Combined effective tax rate"

### Region Default Values

| Region | Default Household Income | Notes |
|--------|-------------------------|-------|
| SF Bay Area | $400,000 | Tech dual-income |
| New York City | $350,000 | Finance/tech mix |
| Los Angeles | $250,000 | Entertainment/tech |
| Seattle | $300,000 | Tech hub |
| Boston | $275,000 | Biotech/finance |

---

## Outputs

### Hourly Rate Display

**Primary output** (prominent display):
- **Pre-tax hourly rate**: `$X.XX/hour`
- **Post-tax hourly rate**: `$Y.YY/hour` (this is the main decision number)

**Dual-earner mode shows**:
- Person A: Pre-tax $X/hr, Post-tax $Y/hr
- Person B: Pre-tax $X/hr, Post-tax $Y/hr
- Household combined rate also shown

### Task Comparison Table

Each row shows:
- **Task name** and typical time range
- **Your time cost** (post-tax hourly rate × hours)
- **Outsource cost** (region-specific estimate)
- **Visual indicator**: Subtle color hint
  - Green tint/icon: Outsourcing costs less than your time
  - Neutral: Roughly equal
  - No indicator: Your time costs less

#### Task List

**Household Tasks**
| Task | Time Estimate | SF Outsource Cost |
|------|---------------|-------------------|
| House cleaning (full) | 2-3 hours | $150-225 |
| Laundry (wash/fold/put away) | 1-2 hours | $40-60 |
| Grocery shopping | 1-2 hours | $30-50 (delivery fees + tip) |
| Meal prep (weekly) | 3-4 hours | $150-300 (meal service) |
| Yard work | 2-3 hours | $100-200 |

**Personal Errands**
| Task | Time Estimate | SF Outsource Cost |
|------|---------------|-------------------|
| Car wash (detail) | 1-2 hours | $50-150 |
| Dry cleaning pickup | 0.5-1 hour | $10-20 (delivery service) |
| Package returns | 0.5-1 hour | $15-25 (TaskRabbit) |
| Waiting for service appt | 2-4 hours | $80-160 (TaskRabbit) |

**Childcare Tasks**
| Task | Time Estimate | SF Outsource Cost |
|------|---------------|-------------------|
| School pickup/dropoff | 0.5-1 hour | $30-50 (per trip) |
| Activity transport | 1-2 hours | $50-100 |
| Homework help (tutoring) | 1-2 hours | $60-150 |

---

## UI/UX Design

### Layout

1. **Header**
   - Title: "Time-Money Trade-Off Calculator"
   - Brief intro paragraph (see Philosophy section)

2. **Input Section**
   - Region dropdown (first, since it affects defaults)
   - Income mode toggle
   - Income field(s)
   - Hours/weeks/tax rate in a row

3. **Results Section** (updates real-time)
   - Prominent hourly rate display box
   - Task comparison table

4. **Assumptions Section** (expandable/collapsible)
   - "Edit assumptions" link/button
   - Reveals editable fields for each task's:
     - Time estimate (hours)
     - Outsource cost ($)
   - Disclaimer: "These are best-effort estimates for your area. Adjust as needed."

5. **Footer**
   - Back to tools link

### Behavior

- **Real-time calculation**: Results update as user types (debounced)
- **No validation errors**: Accept any numeric input
- **Persistent state**: Optional - consider localStorage for return visits
- **Mobile responsive**: Stack inputs vertically on mobile

### Visual Hints for Comparison

Use subtle visual cues, not explicit "outsource this!" text:

```
Task                    Your Time    Outsource
House cleaning (2-3hr)  $300         $180         [slight green bg]
Grocery shopping (1hr)  $100         $40          [slight green bg]
Car wash (1hr)          $100         $75          [neutral]
```

---

## Philosophy / Intro Text

**Brief intro** (always visible):
> "Understanding the value of your time can help make outsourcing decisions clearer. Enter your income and work hours to see what your time is really worth."

**Personal note** (part of intro):
> "I've found it hard to conceptualize outsourcing tasks as an option. This calculator provides a simple view of time-value for various income levels to help make these trade-offs concrete."

---

## Technical Implementation

### Calculation Formulas

```javascript
// Annual hours worked
annualHours = hoursPerWeek * weeksPerYear

// Pre-tax hourly rate
preTaxHourly = annualIncome / annualHours

// Post-tax hourly rate (the decision number)
postTaxHourly = preTaxHourly * (1 - taxRate/100)

// Your time cost for a task
yourTimeCost = postTaxHourly * taskHours
```

### Data Structure

```javascript
const REGIONS = {
  sf: {
    name: 'SF Bay Area',
    defaultIncome: 400000,
    tasks: {
      houseCleaning: { hours: [2, 3], cost: [150, 225] },
      laundry: { hours: [1, 2], cost: [40, 60] },
      // ...
    }
  },
  // ...
};
```

### File Structure

Single HTML file with:
- Embedded CSS (following existing tool patterns)
- Embedded JavaScript
- No external dependencies

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| $0 income | Show $0/hour, comparisons still work |
| 0 hours/week | Show infinity or "N/A" |
| Very high income ($10M+) | Just calculate, no warning |
| Very long hours (80+/week) | Just calculate, shows lower hourly rate |
| Negative values | Treat as 0 or allow (math still works) |

---

## Out of Scope

- Custom task addition (decided against for simplicity)
- "Who should do this task" logic for dual-earners
- Formal citations for outsourcing costs
- Strict input validation
- Time tracking or history features
- Integration with actual service providers

---

## Implementation Checklist

- [ ] Create `time-money-calculator.html`
- [ ] Implement region selector with defaults
- [ ] Implement income mode toggle (single/dual)
- [ ] Build real-time calculation logic
- [ ] Create task comparison table with all three categories
- [ ] Add subtle color-coding for comparison hints
- [ ] Build expandable assumptions editor
- [ ] Add intro text with personal note
- [ ] Test mobile responsiveness
- [ ] Update `index.html` with new tool
- [ ] Update `colophon.html` with new tool

---

## Tradeoffs Accepted

1. **Fixed task list over custom tasks**: Simpler UX, but less flexible
2. **No explicit recommendations**: Respects user autonomy but may be less actionable
3. **Approximate outsourcing costs**: "Best effort" rather than precise, but avoids staleness
4. **No formal citations**: Cleaner design, relies on editability instead

---

*This spec was developed using the `/enrich-plan` skill to systematically clarify requirements.*
