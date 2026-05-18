# Complete Guide: Building a Wyld Sales Data Coordinator Workflow in PowerPoint

This guide will walk you through creating a **professional, interview-ready** visual that maps the entire order lifecycle. Follow these steps exactly.

---

## Part 1: Before You Start - Setup

### What You'll Need
- PowerPoint (any version)
- The job description (open in another window)
- The Excel workbook (for reference)

### Slide Setup
1. Open PowerPoint → **Blank Presentation**
2. Delete any default text boxes
3. Set orientation: **Design** → **Slide Size** → **Widescreen (16:9)**
4. Choose a clean color scheme:
   - **Wyld's brand colors** (based on their site): Deep Green `#1B4D3E`, Cream `#F5F0E6`, Orange accent `#E87A2A`
   - **Or use generic professional:** Dark Blue `#1E3A5F`, Light Gray `#F0F4F8`, Accent `#E67E22`

---

## Part 2: The Four Diagrams to Build

You'll create **4 interconnected visuals** that tell the complete story:

| Slide # | Visual Name | Purpose |
|:---|:---|:---|
| 1 | The Order Lifecycle (Swimlane) | Main workflow - 15 minutes to build |
| 2 | Cross-Functional Communication Map | Who you work with - 10 minutes |
| 3 | Systems & Data Flow (CRM → ERP) | Technical depth - 10 minutes |
| 4 | Exception & Hold Decision Tree | Compliance detail - 10 minutes |

**Total time:** ~45 minutes for all four slides

---

## Part 3: Detailed Build Instructions

---

### 📊 SLIDE 1: The Order Lifecycle Swimlane (Most Important)

This is your masterpiece. It shows the **end-to-end order journey** with YOU at the center.

#### Step 1: Create the Background Layout

```
1. Insert → Shapes → Rectangle (draw full slide)
2. Right-click → Format Shape → Fill → Light Gray (#F0F4F8)
3. Insert → Text Box → Top center: "Wyld Sales Data Coordinator: End-to-End Order Lifecycle"
   Font: 28pt, Bold, Dark Blue
4. Subtitle: "From CRM Entry to Invoiced & Reconciled"
   Font: 16pt, Italic, Gray
```

#### Step 2: Build the Four Horizontal Swimlanes

You'll create **4 swimlanes** stacked vertically. Each represents a Phase.

| Phase | Color | Height |
|:---|:---|:---|
| Phase 1: Entry & Compliance | Light Green (#E8F5E9) | 20% of slide |
| Phase 2: Fulfillment Coordination | Light Blue (#E3F2FD) | 20% |
| Phase 3: Invoicing & Reconciliation | Light Yellow (#FFF9C4) | 20% |
| Phase 4: Post-Sale & Credits | Light Orange (#FFF3E0) | 20% |

**How to draw a swimlane:**
```
Insert → Shapes → Rectangle
Draw across full width, specific height
Right-click → Format Shape → Fill → Choose color
Add border: Line → Solid → Dark Gray, 1pt
Insert → Text Box → Type "Phase 1: Entry & Compliance" (inside the rectangle, top-left corner)
```

Repeat for all 4 phases, stacking them vertically.

#### Step 3: Add the Process Steps (Connecting Arrows)

**Phase 1: Entry & Compliance (Green lane)**

Add these shapes in a horizontal row (left to right):

| Step | Shape Type | Text | Color |
|:---|:---|:---|:---|
| 1 | Oval (Start) | "Order Received<br>from CRM" | Green Fill |
| 2 | Rectangle | "Check License<br>Status" | White |
| 3 | Diamond (Decision) | "Valid License?" | White |
| 4 | Rectangle | "Check METRC<br>Manifest ID" | White |
| 5 | Diamond | "Manifest Present?" | White |
| 6 | Rectangle | "Check SKU<br>Restrictions" | White |
| 7 | Diamond | "SKU Approved?" | White |
| 8 | Oval (End of Phase) | "Order Status:<br>APPROVED" | Green Fill |

**How to add decision diamonds:**
```
Insert → Shapes → Diamond (under Basic Shapes)
Format → Size → Width 1.5", Height 1.5"
```

**How to add arrows between them:**
```
Insert → Shapes → Line Arrow
Draw from center of one shape to center of next
Format → Line Weight → 2pt
```

**Add the "FAIL" branches (very important for compliance):**

From each diamond, add a downward arrow to a **Red Rectangle** below:

```
Diamond (Valid License?) → No → Red Rectangle: "Flag Compliance Hold"
Diamond (Manifest Present?) → No → Red Rectangle: "Flag: Missing Manifest"
Diamond (SKU Approved?) → No → Red Rectangle: "Flag: Restricted SKU"

Then from each Red Rectangle → Arrow right to: "Notify Sales Rep & Compliance Team"
Then back up to the diamond (loop back to re-check)
```

**Phase 2: Fulfillment Coordination (Blue lane)**

Repeat the process (horizontal row):

```
[Check Available Inventory] → [Available? - Diamond] → Yes → [Release to Warehouse]
                                                          ↓ No
                                                    [Flag: Short Order]
                                                          ↓
                                                    [Coordinate with Inventory Team]
                                                          ↓
                                                    [Adjust Order or Create Backorder]
                                                          ↓
                                                    [Return to Check Inventory]
```

**Phase 3: Invoicing & Reconciliation (Yellow lane)**

```
[Receive Shipment Confirmation] → [Generate Invoice in ERP] → [Compare Invoice vs. CRM]
                                                                      ↓
                                                [Match? - Diamond] → Yes → [Order: Fulfilled & Invoiced]
                                                                      ↓ No
                                                [Flag: Variance or Orphan Invoice]
                                                                      ↓
                                                [Investigate with Accounting]
                                                                      ↓
                                                [Adjust & Reconcile] → (loop back)
```

**Phase 4: Post-Sale & Credits (Orange lane)**

```
[Customer Issue Reported?] → Yes → [Open Support Case] → [Issue Type? - Diamond]
                                                              ↓
                                    Damaged → [Process Credit Memo] → [Update AR Aging]
                                    Shortage → [Coordinate Refund/Reship] → [Close Case]
                                    ↓
                            [Order Complete - Archive Data]
```

#### Step 4: Add Your Role Highlight

This is critical. Add a **vertical callout** on the left side that spans all 4 phases:

```
Insert → Shapes → Rounded Rectangle (draw vertically on left edge, covering all 4 lanes)
Fill → Deep Blue (#1E3A5F)
Text (rotated 90 degrees, white, bold, 20pt): "SALES DATA COORDINATOR: Owns Every Step"
```

Add a **small icon** of a person or clipboard next to the text.

#### Step 5: Add State Compliance Callouts

At the bottom of Slide 1, add a small note box:

```
Insert → Text Box → Bottom right corner
Text: "State-Specific Rules Applied Per Order: METRC License ✓ | Manifest ID ✓ | SKU Restriction ✓ | Age Verification ✓"
Fill → Light Gray, Italic, 10pt font
```

---

### 📊 SLIDE 2: Cross-Functional Communication Map

This shows **who you talk to** and **what you coordinate**.

#### Step 1: Center Hub

```
Insert → Circle (center of slide) → Size: 3" diameter
Fill → Deep Blue (#1E3A5F)
Text (white, bold, 14pt): "Sales Data<br>Coordinator"
```

#### Step 2: Add the Five Spoke Teams

Add **5 rounded rectangles** around the center hub (like a star):

```
Top Left: "SALES TEAM"
   Sub-text: "Order changes, rejections, holds"
   Arrow: ↔️ bidirectional
   Color: Orange accent

Top Right: "WAREHOUSE / DISTRIBUTION"
   Sub-text: "Shipments, short ships, OTIF"
   Arrow: ↔️ bidirectional

Bottom Left: "INVENTORY"
   Sub-text: "Stock availability, allocations"
   Arrow: ↔️ bidirectional

Bottom Right: "ACCOUNTING"
   Sub-text: "Invoicing, credit memos, AR"
   Arrow: ↔️ bidirectional

Bottom Center: "COMPLIANCE"
   Sub-text: "Licenses, manifests, SKU rules"
   Arrow: ↔️ bidirectional
```

#### Step 3: Add Communication Lines

```
Insert → Shapes → Line (Curve or Elbow Connector)
Draw from center hub to each team rectangle
Line weight: 3pt
Line color: Dark Blue
```

**To make bidirectional arrows:**
- Use **Line with Arrow** (points both directions) OR
- Add two arrows (one pointing each way)

#### Step 4: Add the "What You Provide" Table

Below the hub diagram, insert a table:

```
Insert → Table → 2 columns x 5 rows

Column 1 Header: "Team"
Column 2 Header: "You Provide"

Rows:
Sales → "Order status updates, compliance hold notifications"
Warehouse → "Approved orders, priority flags, return authorizations"
Inventory → "Real-time shortage alerts, allocation adjustments"
Accounting → "Reconciled invoices, variance reports, credit memo docs"
Compliance → "Flagged orders, license expiration reports, audit trail"
```

#### Step 5: Add Title

```
Top of slide: "Cross-Functional Communication: How You Enable the Whole Business"
Font: 24pt, Bold, Dark Blue
```

---

### 📊 SLIDE 3: Systems & Data Flow (CRM → ERP)

This shows the **technical workflow** and your role in data integrity.

#### Step 1: Create Three Vertical Columns

| Left Column (30% width) | Middle Column (40% width) | Right Column (30% width) |
|:---|:---|:---|
| **SYSTEMS** | **YOUR ACTIONS** | **OUTPUTS** |
| Light Blue fill | Light Green fill | Light Orange fill |

#### Step 2: Populate Left Column (Systems)

Stack vertically:

```
[Icon: Cloud] CRM (Salesforce)
      ↓
[Icon: Database] ERP (Business Central)
      ↓
[Icon: Box] WMS (Warehouse)
      ↓
[Icon: Clipboard] METRC (Compliance)
```

Use arrows pointing down between each.

#### Step 3: Populate Middle Column (Your Actions)

Align horizontally with the left column:

```
[Review CRM Orders] → [Validate Compliance] → [Release to ERP]
                          ↓
                    [Flag Exceptions]
                          ↓
                    [Coordinate Fulfillment]
                          ↓
                    [Reconcile Invoices]
                          ↓
                    [Process Credits]
```

#### Step 4: Populate Right Column (Outputs)

```
[Approved Orders]
[Compliance Holds Report]
[Short Ship Alerts]
[Variance Report]
[Credit Memos]
[Reconciliation Summary]
```

#### Step 5: Connect Everything with Arrows

Draw arrows connecting:
- Left column → Middle column (system to your action)
- Middle column → Right column (your action to output)
- Left column items to each other (data flow)

#### Step 6: Add "The Reconciliation Loop" Callout

At the bottom, add a curved arrow looping back from Right Column to Left Column:

```
Text: "THE RECONCILIATION LOOP: CRM orders → ERP invoices → Match → Report"
This shows you close the loop between systems.
```

#### Step 7: Title

```
Top: "Systems & Data Integrity: Closing the Loop Between CRM, ERP, and WMS"
```

---

### 📊 SLIDE 4: Exception & Hold Decision Tree

This shows your **compliance judgment** and is very impressive in an interview.

#### Step 1: Start with a Trigger

```
Top center: Oval → "Order Entered into CRM"
```

#### Step 2: Create the Decision Branches

Create a **tree structure** flowing downward:

```
                                    [Order Entered]
                                          |
                                          v
                              [Check Customer License]
                                          |
                          +---------------+---------------+
                          |                               |
                          v                               v
                   [Valid]                           [Invalid]
                          |                               |
                          v                               v
              [Check METRC Manifest]              [HOLD: License Issue]
                          |                          Notify Sales/Compliance
              +-----------+-----------+
              |                       |
              v                       v
        [Present]                  [Missing]
              |                       |
              v                       v
    [Check SKU Restrictions]    [HOLD: Missing Manifest]
              |                  Notify Sales/Compliance
      +-------+-------+
      |               |
      v               v
 [Approved]      [Restricted]
      |               |
      v               v
[Release to     [HOLD: SKU Not Approved]
 Warehouse]      Notify Sales/Compliance
```

#### Step 3: Add Hold Resolution Paths

For each HOLD box, add a side branch:

```
[HOLD: License Issue] → [Sales Rep Notified] → [Customer Updates License]
                                                      ↓
                                              [Re-Check License]
                                                      ↓
                                              [Valid?] → back to main flow
```

#### Step 4: Add a "Hold Reasons Summary" Table

At the bottom right, insert a table:

| Hold Reason | Owner | Action |
|:---|:---|:---|
| Expired License | Compliance | Customer renews |
| Missing Manifest | Sales Ops | Generate METRC ID |
| Restricted SKU | Sales | Change order or approve exception |
| Inventory Short | Inventory | Allocate or backorder |

#### Step 5: Title

```
Top: "Compliance & Exception Management: Order Hold Decision Tree"
Subtitle: "Applying State-Specific Rules (METRC, Age, SKU) Before Release"
```

---

## Part 4: Making It Look Professional (The Polish)

### Color Palette (Stick to These)

| Use | Color Name | Hex Code |
|:---|:---|:---|
| Main Title | Dark Green | `#1B4D3E` |
| Phase Headers | Dark Blue | `#1E3A5F` |
| Your Role Highlight | Deep Blue | `#0D47A1` |
| Success/Approved | Green | `#2E7D32` |
| Hold/Exception | Red | `#C62828` |
| Warning/Review | Orange | `#E87A2A` |
| Phase 1 Background | Light Green | `#E8F5E9` |
| Phase 2 Background | Light Blue | `#E3F2FD` |
| Phase 3 Background | Light Yellow | `#FFF9C4` |
| Phase 4 Background | Light Orange | `#FFF3E0` |

### Fonts

- **Headings:** Calibri Bold, 24-28pt
- **Shapes text:** Calibri, 12-14pt
- **Subtext:** Calibri Italic, 10pt

### Alignment Tips

- **Select all shapes** → Format → Align → Distribute Horizontally
- **Select all shapes** → Format → Align → Align Middle (for same row)
- Use **Guides** (View → Guides) to keep consistent margins

### Icons to Add (Search in PowerPoint: Insert → Icons)

| Icon | Search Term |
|:---|:---|
| Order/Clipboard | "clipboard" |
| Compliance/Shield | "shield" |
| Warehouse/Box | "box" |
| Accounting/Money | "calculator" |
| Communication | "chat" |
| Data/Database | "database" |
| Hold/Flag | "flag" |

---

## Part 5: How to Present This in an Interview

Walk through the slides in this order:

### Slide 1 (The Lifecycle) - 3 minutes
> *"This is the end-to-end order lifecycle I would own. Starting with CRM entry, I apply a state-specific compliance check—license, METRC manifest, SKU restrictions. Only after passing do I release to the warehouse. After shipment, I reconcile the invoice against the original order. Any mismatch gets flagged. Finally, I handle post-sale credits and returns, closing the loop with Accounting."*

**Point to the HOLD branches** as you say: *"These red boxes are where I add value. I catch compliance issues before they become shipping or billing problems."*

### Slide 2 (Communication Map) - 2 minutes
> *"I sit at the center of five teams. Sales gives me orders. Warehouse gives me ship confirmations. Inventory gives me stock levels. Accounting gives me invoices. Compliance gives me rules. My job is to make sure all five are looking at the same accurate data."*

### Slide 3 (Systems Flow) - 2 minutes
> *"This is the technical layer. CRM orders come in, I validate them, they go to ERP. When a shipment happens, an invoice generates. I reconcile that invoice back to the CRM order. That's the loop. If an invoice exists without a matching order—an 'orphan'—I flag it for Accounting immediately."*

### Slide 4 (Decision Tree) - 2 minutes
> *"This is my compliance logic. Every order hits three gates: license, manifest, SKU. If any fails, the order holds and I notify the right team. I don't just process orders—I ensure only compliant, shippable, billable orders move forward."*

### Close (30 seconds)
> *"The result of this workflow is simple: leadership can trust the revenue number. CRM says 'we sold it,' ERP says 'we billed it,' warehouse says 'we shipped it.' My job is to make sure those three always match."*

---

## Part 6: Save & Export

1. **Save the PowerPoint file** as `Wyld_Sales_Data_Coordinator_Workflow.pptx`
2. **Export as PDF** (File → Export → Create PDF) for easy sharing
3. **Export key slides as PNG** (File → Export → Change File Type → PNG) to embed in portfolio or email

---

## Part 7: Final Checklist Before Interview

| Element | Check |
|:---|:---|
| Slide 1 has all 4 phases | ☐ |
| Slide 1 shows HOLD branches in red | ☐ |
| Slide 2 has all 5 teams | ☐ |
| Slide 2 has bidirectional arrows | ☐ |
| Slide 3 shows CRM → ERP → Reconciliation loop | ☐ |
| Slide 3 shows "orphan invoice" flag | ☐ |
| Slide 4 has decision diamonds for each compliance check | ☐ |
| Slide 4 has hold resolution paths | ☐ |
| Consistent color scheme across all slides | ☐ |
| Your name and date on the first slide | ☐ |
| Fonts are readable (not too small) | ☐ |

---

## Quick Reference: Shape Cheat Sheet

| Shape | Use For |
|:---|:---|
| **Oval** | Start/End of process |
| **Rectangle** | Action/Process step |
| **Diamond** | Decision (Yes/No) |
| **Rounded Rectangle** | Phase/Swimlane labels |
| **Arrow** | Flow direction |
| **Document** | Report/output |
| **Cylinder** | Database/system |

---

**You now have a complete, interview-ready visual model.** Take your time building it. The act of creating it will help you internalize the workflow.

Good luck with the Wyld interview! 🚀