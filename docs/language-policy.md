# Repository Language Policy

This policy applies only to TaskForge source maintenance and its distribution
examples. It does not set the language of recipient projects or user-owned content.

## Shared sources

Use English for shared instructions, operational guides, historical reports,
source comments, command help, role descriptions and test explanations. Keep
existing file paths, headings referenced by loaders, configuration keys, model
IDs, command syntax and HTML markers stable.

The language of these instructions does not select the user's response language.
Follow the user's requested language and output contract.

## User guides

- `README.md` is the Korean user guide. Write ordinary explanations and link
  labels in Korean; retain product names, commands, file names and setting keys.
- `README.en.md` is the matching English guide. Keep commands, references and
  safety boundaries aligned with the Korean guide.
- `README.ko.md` remains a Korean compatibility pointer to `README.md`.

Use a named product or literal UI label when needed. Explain an unfamiliar
technical term in the guide's language rather than switching languages mid-sentence.

## Localized data and examples

Korean is intentional in language selectors, quoted user requests, multilingual
routing tests, localized assertion data and existing interface values. Label the
language of these examples; do not translate them as ordinary prose.

The Notion recorder retains its existing Korean `type` values and Korean output
template labels. English instructions must identify these as localized contract
data. A prose translation must not rename fields or change accepted values.

Historical reports may be translated for readability. Preserve their dates,
versions, observations, commands and limitations; do not turn historical evidence
into a claim about the current release.

## Maintenance checks

Update canonical sources before generated documents. Check links, referenced
headings, TOML parsing, language-specific assertions and runtime size budgets.
Translation must preserve test inputs and safety requirements. Update an
assertion's language without reducing the behavior it checks.
