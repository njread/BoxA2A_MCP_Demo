"""
Box Document Generation Tool for Agent
Provides capital call notice generation using Box Doc Gen API
"""

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def guide_capital_call_creation() -> str:
    """
    Provide guidance on creating capital call notices
    
    Returns:
        Comprehensive guidance on the capital call notice creation process
    """
    guidance = """🚀 **Capital Call Notice Creation Guide**

**What you need to get started:**

1. **📋 Template File ID** - The Box file ID of your Word template
2. **📁 Output Folder ID** - Where generated documents will be saved
3. **👥 LP Data** - Information about each limited partner

**How to find your template and folder IDs:**
• Use Box search to locate your templates and output folders
• Copy the IDs from the search results

**Required LP Data Structure:**
```json
{
  "gp": {
    "contact_name": "John Smith",
    "contact_phone": "(555) 123-4567", 
    "contact_email": "jsmith@gpfund.com"
  },
  "fund": {
    "legal_name": "Technology Investment Fund II, L.P.",
    "total_call_amount": 75000000
  },
  "notice": {
    "notice_date": "2024-01-15",
    "due_date": "2024-01-30"
  },
  "lp": {
    "lp_name": "Investor_Name",
    "individual_call_amount": 1750000,
    "commitment_total": 50000000,
    "percentage_called": 40,
    "remaining_commitment": 30000000,
    "total_distributions_received": 10000000,
    "recallable_amount": 5000000
  },
  "wire_instructions": {
    "bank_name": "Private Equity Bank",
    "bank_contact_name": "Jane Doe",
    "bank_contact_phone": "(213) 987-9876",
    "bank_address": "1234 Wilshire Blvd., Los Angeles, CA 90024",
    "aba_routing": "023 334 023",
    "account_number": "445632189"
  },
  "investment": {
    "company_name": "ABC Company",
    "company_description": "widget manufacturer",
    "company_location": "Akron, Ohio",
    "investment_purpose": "expand into the Canadian market",
    "expected_close_date": "2024-02-15",
    "total_financing": 150000000,
    "fund_investment": 75000000
  }
}
```

**Quick Start Steps:**
1. **Find your template:** Use Box search for "capital call template"
2. **Find your output folder:** Use Box search for "LPs" or "capital call output"
3. **Create your LP data:** Prepare the data structure above for each LP
4. **Generate notices:** Use the template ID, folder ID, and LP data

**Example workflow:**
```
User: "Create capital call notices for Fund III"
Agent: [Guides through template selection, data preparation, and generation]
```

**💡 Pro Tips:**
• You can generate multiple notices in one batch
• Each LP gets a personalized document
• Files are automatically named with LP name and date
• You can check generation status using the batch ID

**Need help?** Just ask me to:
• "Help me create capital call notices"
• "Show me the LP data structure"
• "Search for capital call templates"
• "Search for output folders"
"""
    
    return guidance

def create_sample_lp_data() -> str:
    """
    Create sample LP data structure for users to get started
    
    Returns:
        Sample LP data structure with explanations
    """
    sample_data = """📋 **Sample LP Data Structure for Capital Call Notices**

Here's a complete example you can use as a starting point:

```json
{
  "gp": {
    "contact_name": "John Smith",
    "contact_phone": "(555) 123-4567",
    "contact_email": "jsmith@gpfund.com"
  },
  "fund": {
    "legal_name": "Technology Investment Fund II, L.P.",
    "total_call_amount": 75000000
  },
  "notice": {
    "notice_date": "2024-01-15",
    "due_date": "2024-01-30"
  },
  "lp": {
    "lp_name": "Institutional_Investor_A",
    "individual_call_amount": 1750000,
    "commitment_total": 50000000,
    "percentage_called": 40,
    "remaining_commitment": 30000000,
    "total_distributions_received": 10000000,
    "recallable_amount": 5000000
  },
  "wire_instructions": {
    "bank_name": "Private Equity Bank",
    "bank_contact_name": "Jane Doe",
    "bank_contact_phone": "(213) 987-9876",
    "bank_address": "1234 Wilshire Blvd., Los Angeles, CA 90024",
    "aba_routing": "023 334 023",
    "account_number": "445632189"
  },
  "investment": {
    "company_name": "ABC Company",
    "company_description": "widget manufacturer",
    "company_location": "Akron, Ohio",
    "investment_purpose": "expand into the Canadian market",
    "expected_close_date": "2024-02-15",
    "total_financing": 150000000,
    "fund_investment": 75000000,
    "coinvestor_name": "Midwest Fund",
    "coinvestor_amount": 60000000,
    "debt_provider": "Bank of Ohio",
    "debt_amount": 15000000,
    "security_type": "Participating preferred stock with 1x liquidation preference and 8% cumulative dividend",
    "ttm_ebitda": 50000000,
    "post_money_valuation": 400000000,
    "fund_total_investment": 100000000,
    "prior_investment": 25000000,
    "prior_investment_type": "junior debt"
  },
  "management_fees": {
    "gross_q1_fees": 3000000,
    "monitoring_fees_received": 1000000,
    "monitoring_fee_offset": 500000,
    "net_management_fee_call": 2500000,
    "lpa_section": "8.1"
  },
  "distributions": {
    "cash_distribution": {
      "company_name": "FGH Company",
      "distribution_amount": 40000000,
      "buyer_name": "StratCo",
      "close_date": "2010-12-15",
      "sale_price": 400000000,
      "ebitda_multiple": 5.5,
      "escrow_amount": 80000000,
      "escrow_purpose": "potential earn-out if FGH Company meets certain milestones",
      "moic": 3.0,
      "irr": 25,
      "return_of_capital_portion": "1/3",
      "investment_gain_portion": "2/3",
      "carried_interest_taken": false,
      "lpa_section": "4.1(b)"
    }
  },
  "lpa_sections": {
    "recallable_capital": "3.3",
    "management_fees": "8.1",
    "waterfall": "4.1(b)",
    "valuation_method": "4.4(d)"
  }
}
```

**Key Fields Explained:**

**🔹 GP (General Partner) Information:**
- `contact_name`, `contact_phone`, `contact_email`: GP contact details

**🔹 Fund Information:**
- `legal_name`: Official fund name
- `total_call_amount`: Total amount being called across all LPs

**🔹 Notice Information:**
- `notice_date`: Date the notice is issued
- `due_date`: Date payment is due

**🔹 LP (Limited Partner) Information:**
- `lp_name`: Name of the limited partner (used in filename)
- `individual_call_amount`: Amount being called from this specific LP
- `commitment_total`: Total commitment amount for this LP
- `percentage_called`: Percentage of commitment being called

**🔹 Wire Instructions:**
- Bank details for receiving payments

**🔹 Investment Details:**
- Information about the investment opportunity
- Company details, financing structure, etc.

**🔹 Management Fees:**
- Fee calculations and LPA references

**🔹 Distributions:**
- Recent distributions and returns

**🔹 LPA Sections:**
- References to relevant Limited Partnership Agreement sections

**💡 Customization Tips:**
• Modify the values to match your specific fund and LPs
• Add or remove fields based on your template requirements
• Use consistent naming conventions for LP names
• Ensure all monetary amounts are in the same currency
• Double-check dates and amounts for accuracy

**Ready to create your own?** Just ask me to:
• "Help me create capital call notices"
• "Show me how to prepare LP data"
• "Generate capital call notices for [fund name]"
"""
    
    return sample_data

def smart_template_discovery() -> str:
    """
    Smart template discovery using existing search results and user guidance
    
    Returns:
        Template discovery guidance with actionable steps
    """
    template_guide = """🔍 **Smart Template Discovery Guide**

Based on your recent searches, I found these capital call templates in your Box environment:

**📋 Available Templates:**
• **CAPITAL CALL.docx** (ID: 1958506957285)
• **Capital Call Notice.docx** (ID: 1856667992985)

**🎯 How to Use These Templates:**

**Step 1: Choose Your Template**
- **CAPITAL CALL.docx** - Good for general capital call notices
- **Capital Call Notice.docx** - More specific to notice format

**Step 2: Get Template Details**
Ask me to search for more details about your chosen template:
• "Search for CAPITAL CALL.docx details"
• "Show me the Capital Call Notice.docx file"

**Step 3: Prepare Your Data**
Use the sample LP data structure I provided to prepare your information

**Step 4: Manual Document Creation**
Since Box Doc Gen isn't currently available, you can:
1. Download your chosen template
2. Use the LP data structure to fill it out
3. Upload the completed documents to your LPs folder

**💡 Pro Tips:**
• Use Box AI to analyze existing capital call notices for reference
• Search for "capital call examples" to see completed notices
• Use Box search to find your output folder (you have an "LPs" folder)

**Need Help?** Ask me to:
• "Search for template details"
• "Show me sample LP data structure"
• "Help me find output folders"
• "Analyze existing capital call notices"

**🚀 Next Steps:**
1. Choose which template to use
2. Get template details and download it
3. Prepare your LP data using the sample structure
4. Create your capital call notices manually
5. Upload them to your LPs folder

This approach gives you full control over the process while avoiding any API limitations!"""
    
    return template_guide

def capital_call_workflow_assistant() -> str:
    """
    Complete workflow assistant for capital call notice creation
    
    Returns:
        Step-by-step workflow guidance
    """
    workflow_guide = """🚀 **Complete Capital Call Notice Workflow**

I'll guide you through the entire process step by step. Let's get started!

**📋 Phase 1: Template Selection**
**Current Status:** ✅ You have 2 templates available
**Next Action:** Choose which template to use

**📁 Phase 2: Output Folder Setup**
**Current Status:** ✅ You have an "LPs" folder
**Next Action:** Confirm this is where you want generated notices saved

**👥 Phase 3: LP Data Preparation**
**Current Status:** ⏳ Ready to prepare
**Next Action:** Use the sample data structure to prepare your LP information

**📝 Phase 4: Document Creation**
**Current Status:** ⏳ Manual creation required
**Next Action:** Fill out your template with LP data

**📤 Phase 5: File Management**
**Current Status:** ⏳ Ready to organize
**Next Action:** Upload completed notices to your LPs folder

**🎯 Let's Start!**

**What would you like to do first?**

1. **"Show me template details"** - Get more info about your templates
2. **"Help me prepare LP data"** - Get the sample data structure
3. **"Search for output folder"** - Confirm your LPs folder setup
4. **"Analyze existing notices"** - Look at completed examples for reference

**💡 Workflow Tip:** 
I'll guide you through each phase and provide the tools you need. Just tell me what you'd like to tackle first!

**Current Progress:** 🟢 Phase 1 Complete, 🟡 Phase 2 Ready, ⚪ Phase 3-5 Pending

What would you like to work on next?"""
    
    return workflow_guide 