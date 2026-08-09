"""SK Hynix valuation band — historical P/E Z-score + ERP.

Layer 0 of concepts/sk-hynix-investment-thesis.md, added 2026-08-09 in
response to a user-supplied external prompt spec (Project_SKH_Alpha_Prompt.md,
Gemini-authored) asking for a standalone P/E band + ERP quant system.
Instead of building a parallel yfinance/DART pipeline, this integrates the
same two indicators into the existing decision engine, reusing data already
verified in the wiki (concepts/rally-justification-analysis.md's quarterly
divergence gauge) rather than duplicating infrastructure.
"""
