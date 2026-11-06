"""Authored Azure Blob Storage curriculum. Regenerate HTML with azure/build.py.

CrimeOS details describe the user-supplied guide dated 2026-11-06. They are
historical branch observations, not a claim that current application code was audited.
"""
from html import escape


def code(text, caption="Worked example · illustrative, no Azure request is sent"):
    return '<div class="snippet"><p class="code-caption">' + escape(caption) + '</p><pre><code>' + escape(text.strip()) + '</code></pre></div>'


def table(headings, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + x + '</th>' for x in headings) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + x + '</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def note(title, body, kind="tip"):
    return '<aside class="callout ' + kind + '"><strong>' + title + '</strong><p>' + body + '</p></aside>'


def flow(items, label="Step-by-step diagram"):
    return '<div class="flow" role="group" aria-label="' + escape(label, quote=True) + '">' + '<span aria-hidden="true">→</span>'.join('<div><b>' + title + '</b><small>' + body + '</small></div>' for title, body in items) + '</div>'


def section(identifier, title, body):
    return '<section class="lesson-section" id="' + identifier + '"><h2>' + title + '</h2>' + body + '</section>'


def predict(question, answer):
    return '<details class="reveal"><summary>Predict first: ' + question + '</summary><div><p>' + answer + '</p></div></details>'


def lab(identifier):
    return '<div data-lab="' + identifier + '"></div><noscript><p>The interactive exercise needs JavaScript. The worked example and prediction above cover the same decision.</p></noscript>'


SNAPSHOT = note("CrimeOS guide snapshot · 6 November 2026", 'Application-specific behavior on this page comes from the supplied guide and its branch audits. This course does not claim a new audit of the current backend or AI repositories. See <a href="reference.html#guide">scope and provenance</a>.')

LESSONS = []


def lesson(identifier, title, minutes, description, objectives, sections, recap):
    LESSONS.append(dict(id=identifier, title=title, minutes=minutes, description=description, objectives=objectives, sections=sections, recap=recap))


lesson("foundations", "Find a file: account, container, blob", 15,
    "Start with a building, a cupboard, and a file. Then learn the three coordinates that identify a blob and why a slash can be part of its name.",
    ["Identify a storage account, container, blob, and blob key.", "Read a standard Blob Storage URL without confusing a path with permission.", "Explain why the same key can identify different files in different places."], [
section("building", "Begin with something familiar",
    '<p>You have a PDF on your laptop. A server and an AI service also need to open it. Azure Blob Storage gives the application a place to keep those bytes and an API for reading and writing them. A <strong>blob</strong> is one stored object: a PDF, image, ZIP, or text file.</p>' +
    flow([("Storage account", "The building · a named Azure storage resource"), ("Container", "A cupboard · a collection of blobs"), ("Blob", "The file · bytes stored under one name")], "Azure storage account contains containers; a container contains blobs") +
    '<p>A storage account is a resource in Azure. A container sits inside that resource; a blob sits inside the container. These are different levels. Creating a database row does not create a blob, and creating a blob does not automatically create a row.</p>'),
section("coordinates", "Every file needs three coordinates",
    code('Storage account: lessonstore\nContainer:       private-files\nKey:             cases/214/complaint.pdf\n\nhttps://lessonstore.blob.core.windows.net/private-files/cases/214/complaint.pdf') +
    table(["Piece", "What it selects", "Example"], [
        ["Storage account / host", "Which Azure storage resource", '<code>lessonstore.blob.core.windows.net</code>'],
        ["Container", "Which collection inside that resource", '<code>private-files</code>'],
        ["Key / blob name", "Which object inside that collection", '<code>cases/214/complaint.pdf</code>'],
    ]) +
    '<p>The storage account name is globally unique in Azure’s storage account namespace and appears in its standard service address. Knowing only <code>cases/214/complaint.pdf</code> is like knowing a file label without knowing the building or cupboard. The identical key in two accounts or two containers identifies two independent blobs. A valid address also does not grant permission to read a private blob; access comes next.</p>' +
    predict('Two accounts both contain <code>cases/214/complaint.pdf</code>. Are these one shared PDF?', 'No. Compare all three coordinates. The account is different, so these are separate stored objects even if their names and bytes happen to match.')),
section("slashes", "A folder view can be a view of names",
    '<p>In a <strong>flat namespace</strong>, <code>case-artifacts/214/run1/derived/x.md</code> is one blob name. The slash characters help people group names; they do not create directory objects. Listing a virtual folder means listing names beginning with its prefix.</p>' +
    code('Prefix: case-artifacts/214/\n\nIncluded: case-artifacts/214/run1/complaint.pdf\nIncluded: case-artifacts/214/run1/derived/x.md\nExcluded: case-artifacts/2140/run1/complaint.pdf') +
    note("Keep the boundary slash", '<code>case-artifacts/214/</code> is a more precise prefix than <code>case-artifacts/214</code>: the latter also begins the name for case 2140.') +
    '<p>The guide describes this flat naming model. Azure also supports a <strong>hierarchical namespace</strong> with directory objects, so “there are no real folders” is a statement about this system’s naming model, not every Azure configuration. <a href="https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-namespace">Microsoft: hierarchical namespace</a>.</p>'),
section("operations", "What reading and writing actually mean",
    table(["Operation", "What changes", "Question to ask"], [
        ["Read / download", "Returns bytes; the blob normally stays where it is", "Do I have the right coordinates and permission?"],
        ["Write / upload", "Stores bytes at a key", "Is overwriting this exact object allowed?"],
        ["List a prefix", "Returns matching names", "Does the prefix include the account root and a boundary slash?"],
        ["Delete", "Removes the addressed object, subject to enabled protection features", "Have I verified which account, container, and key this selects?"],
    ]) +
    '<p>An overwrite-enabled write to an existing key updates that object rather than making a second object with the same name. Whether an API call allows overwrite, requires conditions, or retains an older version depends on the operation and configuration. Do not assume that a new database ID protects an existing blob.</p>'),
section("scope", "What this course means by Azure Storage",
    '<p>Azure Storage also offers file shares, queues, and tables. This learning path concentrates on <strong>Blob Storage</strong>, because CrimeOS documents, OCR text, case bundles, and derived AI files use blobs. You do not need to learn every Azure service before you can follow one PDF.</p>' +
    '<p>For the basic resource model, see <a href="https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction">Microsoft’s Blob Storage introduction</a>. Real names in later CrimeOS examples are labels from the guide; all browser exercises are simulations and use no credentials.</p>'),
section("try", "Explore the three coordinates", lab("explorer")),
], ["A blob is found by storage account + container + exact key.", "In the guide’s flat namespace, slashes are part of the blob name.", "A URL tells you an address; it does not by itself authorize a private read."])

lesson("access", "Open a file without sharing the master key", 18,
    "Understand account-key connection strings, signed links, permissions, expiry, and why the browser and AI receive narrow grants.",
    ["Distinguish a blob name from a secret account access key.", "Predict access from a signed link’s resource, permissions, and validity interval.", "Explain the guide’s account-key signing design and Azure identity alternatives."], [
section("two-keys", "The word key has two different meanings",
    '<p>A <strong>blob key</strong> is a name such as <code>cases/214/complaint.pdf</code>. An <strong>account access key</strong> is a credential. Confusing them makes discussions about “sending the key” dangerous: the AI can receive a blob name as an identifier, but it must not receive the storage account’s secret access key.</p>' +
    table(["Item", "Meaning", "Treat it as a credential?"], [
        ["Blob key", "Name inside a container", "It may reveal sensitive context, but it is not authorization by itself"],
        ["Account-key connection string", "Connection settings containing the account name and secret access key", "Yes; broad account access where Shared Key is allowed"],
        ["Signed link / SAS URL", "Resource URL with a token granting specified access", "Yes; anyone holding it can use its granted access"],
    ])),
section("delegation", "Give the visitor a temporary permission slip",
    flow([("Backend", "Holds the authorized signing credential"), ("Signed link", "One resource + allowed action + expiry"), ("Browser or AI", "Uses the link directly with Azure")], "Backend signs limited access; browser or AI uses the signed URL") +
    '<p>A <strong>shared access signature</strong> (SAS) delegates access. Its scope, permissions, and times are part of what is signed. Merely changing a read flag to a write flag in an existing URL does not grant write access: the signature would no longer match. The backend must issue the appropriate grant.</p>' +
    '<p>In the guide’s implementation, ordinary read links last about <strong>300 seconds</strong>, case-bundle read links about <strong>900 seconds</strong>, and write links about <strong>300 seconds</strong>. These are application defaults, not Azure-wide limits.</p>'),
section("permission", "Check three things before predicting success",
    table(["Check", "Example", "Expected consequence"], [
        ["Resource", "A grant for complaint.pdf is used for another blob", "The other blob is outside the grant"],
        ["Permission", "A write-only grant is used to download", "The operation is not permitted"],
        ["Validity", "A five-minute grant is used after its expiry", "The grant is no longer valid"],
    ]) +
    '<p>These checks describe the token. Real requests can also fail because the blob is missing, network access is blocked, or the request does not meet Azure’s other conditions. Expiry is a ceiling on a grant, not a promise that every request before expiry succeeds.</p>' +
    predict('The AI has a valid write-only link for a text file. Can it read the PDF next to that file?', 'No. The grant covers a specified resource and permissions. A write grant to the text file is not a read grant to the original PDF. The AI asks the backend for the access it needs.')),
section("signing", "What the guide’s signer needs",
    '<p>The guide’s backend signs using the selected storage account’s account key, obtained from its connection string. A connection string containing only an existing SAS token does not supply that signer with an account key, so it cannot use that implementation to mint new account-key-signed links.</p>' +
    note("Azure has more than one authorization method", 'Account-key signing describes this CrimeOS snapshot. Azure also supports Microsoft Entra authorization, managed identities, and user delegation SAS. A SAS can cover broader resources and multiple permissions; the guide deliberately issues narrow per-file grants. <a href="https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview">Microsoft: SAS types and scopes</a>.') +
    '<p>For new Azure designs, Microsoft recommends using Entra credentials and managed identities where possible. That broader guidance does not mean the audited branch already uses them. <a href="https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage">Microsoft: account keys and identity guidance</a>.</p>'),
section("handling", "Keep credentials on the correct side of the boundary",
    '<p>The backend holds the deployment connection string in configuration and customer connection strings encrypted in the database. The browser and AI get the necessary signed links. Neither needs the broad secret to upload one document.</p>' +
    '<p>Do not print a connection string, webhook secret, or signed URL in logs, examples, screenshots, or support messages. Expiry reduces exposure but does not make a signed link public information. If a link expires during a workflow, request a fresh grant through the backend rather than expanding the AI’s privileges.</p>' + SNAPSHOT),
section("try", "Try permissions and time", lab("sas")),
], ["A blob key is a name; an account key is a secret credential.", "A signed link grants only its configured resource, permissions, and validity interval.", "The guide uses account-key signing; Azure also supports identity-based access."])

lesson("ownership", "Find the owner before choosing storage", 18,
    "Separate deployments, Azure storage accounts, and CrimeOS customer accounts. Follow a case through its station to its owning customer.",
    ["Explain the two meanings of account.", "Trace case ownership without substituting the viewing user.", "Understand deployment storage, optional customer storage, and shared-account collision risks."], [
section("deployment", "A deployment is a running copy of the product",
    '<p>Alpha, gamma, demo, staging, and production are deployment names. Each deployment has storage settings. “Storage configured for each deployment” does <strong>not</strong> guarantee that every deployment has a separate Azure storage account.</p>' +
    table(["Setting", "Meaning", "Guide example"], [
        ['<code>AZURE_CONNECTION_STRING</code>', "Deployment storage credential", "Secret; no value belongs in this course"],
        ['<code>AZURE_PRIVATE_CONTAINER</code>', "Container opened by this environment", '<code>private-files</code>'],
        ['<code>STAGE</code>', "Deployment stage", '<code>gamma</code>'],
        ['<code>MEDIAFILES_LOCATION</code>', "Normal deployment media root", '<code>crimeosbackend-gamma/gamma/media</code>'],
    ])),
section("two-accounts", "An Azure account is not a customer account",
    table(["Question", "Azure storage account", "CrimeOS customer Account"], [
        ["What is it?", "A named storage resource in Azure", "A product customer such as a police organisation"],
        ["Where is it defined?", "Azure", '<code>iam</code> app, <code>Account</code> model'],
        ["What does it contain?", "Containers and blobs", "Customer information and optional storage settings"],
        ["How are they connected?", "A credential opens the Azure resource", '<code>storage_prefix</code>, <code>storage_stage</code>, and an encrypted connection string describe customer storage'],
    ]) +
    '<p>When the customer has no dedicated storage configured, its files use the deployment storage. When configured, correctly rooted keys can route to its own storage. Adding customer storage settings alone does not transform every existing bare key.</p>'),
section("owner", "The case’s station is the starting point",
    flow([("Case 9001", "The case whose file is being handled"), ("Station / jurisdiction", "The case’s station"), ("Customer Account", "The station’s owning customer"), ("Storage settings", "That owner’s configured root and connection")], "Case ownership flows through the case station to its customer storage") +
    '<p>The guide’s ownership service first follows the case’s station to its customer account. If the case has no station, it uses the actor’s account when available. If neither can be found, it warns and uses deployment storage. A person merely opening another customer’s case does not become the owner of its files.</p>' +
    predict('A Delhi user opens a case whose station belongs to Maharastra. Which customer should own the new case artifact?', 'Maharastra. Follow the case’s station first. The viewing user is a fallback when ownership cannot be obtained through the case, not a replacement for an existing case owner.')),
section("shared", "The guide’s alpha and gamma example",
    '<p>The guide reports a gamma row with host <code>crimeosbackendalpha.blob.core.windows.net</code>, container <code>private-files</code>, and a key beginning <code>crimeosbackend-gamma/gamma/media/</code>. It describes alpha and gamma sharing that account and container while separating normal files with their key prefixes.</p>' +
    code('Same Azure account and container:\n  crimeosbackend-alpha/alpha/media/case-artifacts/214/a.pdf\n  crimeosbackend-gamma/gamma/media/case-artifacts/214/a.pdf\n\nAn unprefixed name could collide:\n  cases/214/ocr_results/a.txt') +
    note("Naming separation depends on using the names", 'If two environments share a container and both write the same bare key, they address the same blob. Separate prefixes prevent that collision only for code that actually includes them.', "warn") +
    '<p>A prefix is also not an independent Azure credential boundary. CrimeOS must still enforce who can request access, choose the right owner, and issue appropriate grants.</p>'),
section("origin", "Why the feature exists",
    '<p>The account-specific storage feature lets a customer keep its case data in its own Azure storage account. The guide associates it with <code>feature/*/account-storage-origin-20261030</code>. The root has a routing purpose: it makes the file’s owning storage identifiable from the key.</p>' +
    '<p>The ownership implementation is mapped to <code>common/services/account_storage_routing.py</code> and <code>common/adapters/account_service_ownership.py</code>. The next lesson connects this owner lookup to the key helpers and router.</p>' + SNAPSHOT),
section("try", "Follow the resulting route", lab("routing")),
], ["A deployment, an Azure storage account, and a customer Account are different things.", "Find a case owner through its station; use the actor only as the described fallback.", "Customer settings need correctly rooted keys to route files to customer storage."])

lesson("keys", "Read the key; predict the storage", 25,
    "Break a key into five parts, follow the router’s precedence, and choose the owner helper that builds a correctly rooted name.",
    ["Apply the deployment-first, customer-second, fallback-last routing rule.", "Choose among all seven key helpers.", "Recognize unchanged bare keys, ambiguous roots, and the 60-second routing cache."], [
section("parts", "Five useful parts of one name",
    '<p>Take the guide’s customer-owned derived file. This is one blob name, but its parts explain both routing and purpose:</p>' +
    '<div class="key-parts" role="group" aria-label="Five parts of a CrimeOS blob key"><div class="key-part"><b>1 · prefix</b><code>crimeos-backend-maha-police-prod</code></div><div class="key-part"><b>2 · stage</b><code>mahapolice-prod</code></div><div class="key-part"><b>3 · fixed word</b><code>media</code></div><div class="key-part"><b>4 · what and where</b><code>case-artifacts/9001/run-1/derived</code></div><div class="key-part"><b>5 · filename</b><code>x_pages_1-3.md</code></div></div>' +
    '<p>The first three parts form the <strong>media root</strong>. The router matches the stage root <code>&lt;prefix&gt;/&lt;stage&gt;/</code>; <code>media</code> is the next conventional segment. The case ID and filename explain the object but do not independently select the customer’s connection.</p>'),
section("router", "The router reads the start, in this order",
    flow([("1 · Deployment root?", "If it starts with this deployment’s own stage root, use deployment storage"), ("2 · Customer root?", "Otherwise find a matching customer prefix/stage and use its connection"), ("3 · No match?", "Use deployment storage silently")], "Connection routing precedence: deployment root, then customer root, otherwise deployment fallback") +
    '<p>This rule is the guide’s <code>connection_for_key</code> in <code>common/utils/account_storage.py</code>. It chooses storage from the <strong>key’s start</strong>. It does not query the case ID in the middle of a bare key to discover its owner.</p>' +
    table(["Key in demo", "Route", "Reason"], [
        ['<code>crimeosbackend-demo/demo/media/a.txt</code>', "Deployment", "Own deployment root wins first"],
        ['<code>delhi/prod/media/a.txt</code>', "Delhi’s configured storage", "Matches Delhi’s prefix/stage root"],
        ['<code>cases/214/ocr_results/a.txt</code>', "Deployment", "No configured root matches this bare key"],
        ['<code>old-customer/prod/media/a.txt</code>', "Deployment", "No current root matches; looking rooted is not sufficient"],
    ]) +
    note("Working does not prove correct routing", 'A writer and reader can both use a bare key and succeed in deployment storage. That still fails the customer-storage requirement. Check the full key and selected connection rather than only a successful download.', "warn")),
section("helpers", "Choose the helper by who owns the file",
    '<p>The helpers begin with a normal key under <code>settings.MEDIAFILES_LOCATION</code> and replace that media-root start with the owner’s media root when required. They build names; the storage adapter then routes and performs the operation.</p>' +
    table(["Helper", "Use for", "Owner lookup"], [
        ['<code>key_for_case(case_id, legacy)</code>', "Case uploads, results, generated letters", "Case’s account; actor fallback as described"],
        ['<code>key_for_actor(user_id, legacy)</code>', "Profile pictures, signatures, user OSINT uploads", "User’s account"],
        ['<code>key_for_account(account_id, legacy)</code>', "Customer templates or account exports", "The given account"],
        ['<code>key_for_jurisdiction(id, legacy)</code>', "Bulk tools that already know the station", "Station’s account"],
        ['<code>chat_prefix(chat_session_id)</code>', "Chat session files", "Chat’s case account; otherwise chat user’s account"],
        ['<code>case_ai_key(case_id)</code>', "Case context bundle ZIP", "Case’s account"],
        ['<code>key_under_every_account(legacy)</code>', "Searching when the owner is unknown", "Candidates under deployment and every configured customer root"],
    ]) +
    '<p>Searching candidate roots does not by itself authorize a user to read everything found. Keep permission checks and owner selection in their respective service layers.</p>'),
section("worked", "Watch the root replacement",
    code('Deployment MEDIAFILES_LOCATION:\n  crimeosbackend-demo/demo/media\nDelhi account root:\n  delhi/prod/media\n\nNormal legacy key:\n  crimeosbackend-demo/demo/media/case_context_data/214.zip\nAfter case_ai_key(214), when case 214 belongs to Delhi:\n  delhi/prod/media/case_context_data/214.zip\nRouter result:\n  Delhi connection + environment container + returned key') +
    '<p>The helper’s input has to begin with the expected deployment media root. If the input is merely <code>cases/214/ocr_results/a.txt</code>, the guide says the helper returns it <strong>unchanged</strong>. Calling the right helper with the wrong input shape does not fix a bare key.</p>' +
    predict('You call <code>key_for_case(214, "cases/214/a.txt")</code>. Does the helper add Delhi’s root?', 'No. The input does not start with MEDIAFILES_LOCATION, so the described replacement does not apply. First build the normal media-rooted key, then pass it through the ownership helper.')),
section("edge-cases", "Two details that affect debugging",
    '<p>The guide describes a <strong>60-second cache</strong> for the routing list. Immediately changing a customer’s prefix, stage, or connection can leave a process using cached routing briefly. Check configuration and cache behavior before concluding a new key is ignored.</p>' +
    '<p>If two customer accounts claim the same prefix/stage root but different connection strings, the guide says the router logs an error and uses the deployment connection. This is an ambiguous configuration, not a safe way to share customer storage. The deployment-root match also takes precedence over customer matching.</p>' +
    predict('Demo knows only <code>acme/prod/</code>, but a saved key starts <code>mh-prefix/prod/media/</code>. Which storage is selected?', 'Deployment storage. No configured account root matches that saved start. The key is not rewritten merely because the case now belongs to Acme.') + SNAPSHOT),
section("try", "Change the key and observe the route", lab("routing")),
], ["Routing precedence is own deployment root, then customer root, then silent deployment fallback.", "Helpers replace an expected MEDIAFILES_LOCATION start; bare strings remain bare.", "Duplicate roots with different credentials cause an error and fallback; routing is cached for 60 seconds."])

lesson("paths", "Saved paths and rebuilt paths behave differently", 22,
    "Learn which values the database stores, how the CrimeOS URL reader extracts a key, and what an ID change can and cannot repair.",
    ["Classify a file as saved-path or built-path and identify its source of truth.", "Locate artifact and OCR paths in the guide’s database model.", "Explain why the saved host does not choose storage inside the described CrimeOS reader."], [
section("two-strategies", "A saved address versus a recipe for an address",
    flow([("Saved path", "Database records the key or URL created when the file was written"), ("Read later", "Use that saved value, even if it contains an old ID")], "Saved-path reading preserves the original object address") +
    flow([("Built path", "Code combines the current inputs into a key"), ("Read or regenerate", "Use the resulting key; generation requires an explicit workflow")], "Built-path reading computes a key from current inputs") +
    table(["Question", "Saved path", "Built path"], [
        ["What does the database hold?", "The file’s full key or URL", "No saved object address for that file; it may hold generation status"],
        ["How is the key obtained?", "Read the saved value", "Build it from case or business identifiers"],
        ["What if the case ID changes?", "The saved old-ID name stays the same", "A DB-ID-based recipe computes a new name"],
        ["Can missing bytes reappear?", "Not from the path alone", "Only if a generation workflow recreates them from available inputs"],
    ]) +
    '<p>“Built” does not mean Azure automatically regenerates a missing file. It means the application can know its name without a saved path. Whether regeneration runs, and which data it needs, depends on the workflow.</p>'),
section("database", "Where the guide says saved values live",
    table(["File / purpose", "Model and table", "Column or JSON member"], [
        ["Original upload or filed letter", '<code>CaseArtifact</code> · <code>investigations_caseartifact</code>', '<code>meta_data.file_url</code>'],
        ["AI-derived extracted text", "Same artifact row", '<code>meta_data.extracted_text_key</code>'],
        ["Artifact lookup hash", "Same artifact row", '<code>file_path_hash</code> is a hash derived from the key, not the key itself'],
        ["Case-document OCR text", '<code>CaseAdditionalDetails</code> · <code>cases_caseadditionaldetails</code>', '<code>case_document_metadata.case_document_ocr_url</code>'],
    ]) +
    '<p>The guide describes <code>meta_data</code> as JSON in a text column and derives table names from model code using Django’s default naming. It did not verify a live database schema. Check the actual schema before adapting a query.</p>'),
section("url", "What the CrimeOS URL reader keeps",
    code('Saved URL:\nhttps://crimeosbackendalpha.blob.core.windows.net/private-files/cases/6453/ocr_results/a.txt\n\nget_object_key_from_file_url(...) keeps:\ncases/6453/ocr_results/a.txt\n\nThen the current environment selects:\nconnection_for_key(key) + its own container + key') +
    table(["Saved URL component", "Used by the described reader?", "What happens"], [
        ["Host", "No", "Discarded when extracting the object key"],
        ["First path segment: container", "No", "Removed; the reading environment opens its configured container"],
        ["Remaining path: key", "Yes", "Its beginning is used for connection routing"],
    ]) +
    note("This is application behavior", 'A client opening an ordinary Azure URL directly contacts that URL’s host. This lesson describes a CrimeOS helper that parses a saved URL and then makes a different request through the storage adapter. Do not generalize “the host is ignored” to Azure itself.', "warn")),
section("changes", "Keep saved addresses stable on reads",
    '<p>Suppose an upload was saved at <code>delhi/prod/media/case-artifacts/214/run-1/a.pdf</code>. A migration gives the case ID 9001. The saved address can still find the old-ID object if the route, container, and object remain correct. Constructing <code>.../9001/...</code> on read asks for another object.</p>' +
    '<p>A validator can also break the valid old path by insisting that it begins with a prefix rebuilt from the new ID. Review the reader, writer, and validator together. If a path must be rewritten, treat that as an explicit migration involving both bytes and references.</p>' +
    predict('The database still holds an upload’s old-ID URL and the file exists. Must its filename be changed to the new case ID?', 'Not merely to read it. Read the saved path and route its key correctly. Renaming without updating all references creates another consistency problem. A current-ID validator may still need correction.') + SNAPSHOT),
section("try", "Change the ID and compare both strategies", lab("paths")),
], ["Saved files are read using their stored address; built files use a recipe.", "The CrimeOS URL-to-key helper discards the saved host and container before routing.", "An old ID in a saved key can be valid; a newly built validator can wrongly reject it."])

lesson("backend-ai", "Let the backend grant access to the AI", 20,
    "Follow the storage-grants endpoint: who chooses keys, who signs access, and how an AI-generated file returns to the artifact record.",
    ["Assign key choice, credentials, and file transfer to the correct service.", "Compare READ_CASE_BUNDLE and WRITE_DERIVED payloads and results.", "Avoid confusing AI request identifiers with artifact IDs."], [
section("boundary", "One service chooses storage; another uses grants",
    table(["Responsibility", "Backend", "AI service"], [
        ["Choose case-data blob keys", "Yes; resolves ownership and builds keys", "No; uses keys returned by the backend"],
        ["Hold storage connection strings", "Deployment configuration and encrypted customer credentials", "No case-data connection string in the described design"],
        ["Sign a read or write link", "Yes, with the routed account credential", "Requests a grant"],
        ["Transfer derived text bytes", "Provides authorized destination", "Writes directly with its signed link"],
    ]) +
    '<p>The guide reports removal of <code>AZURE_STORAGE_CONNECTION_STRING</code> from the AI’s case-data path. The AI does not need to reimplement customer-storage routing. It uses the destinations and permissions chosen by the backend.</p>'),
section("endpoint", "The storage-grants request",
    code('POST /api/cases/ai_data/storage_grants/v1/', "Guide endpoint · reference only, no request is executed") +
    '<p>The request includes the shared webhook secret, <code>case_id</code>, <code>operation</code>, and <code>payload</code>. Use the API’s documented secret-field name in real code; no secret value is included here. The backend checks that the case exists and is not archived, resolves its owner, constructs the key, and signs the permitted access.</p>' +
    table(["Operation", "Payload", "Result", "Key under the owner’s media root"], [
        ['<code>READ_CASE_BUNDLE</code>', "Empty", "Read link; about 900 seconds", '<code>case_context_data/&lt;case_id&gt;.zip</code>'],
        ['<code>WRITE_DERIVED</code>', '<code>run_id</code> and <code>file_names</code>', "One key and write link per filename; about 300 seconds", '<code>case-artifacts/&lt;case_id&gt;/&lt;run_id&gt;/derived/&lt;file_name&gt;</code>'],
    ]) +
    '<p>For example, a customer media root <code>delhi/prod/media</code> produces <code>delhi/prod/media/case_context_data/214.zip</code>. The media root belongs in both the key-building and signing paths.</p>'),
section("round-trip", "The returned key must make the round trip",
    flow([("1 · AI requests", "Operation, case ID, run ID and sanitized filename inputs"), ("2 · Backend grants", "An owner-rooted key and a narrow signed URL"), ("3 · AI writes", "Uploads the derived bytes to the granted destination"), ("4 · Backend saves", "Returned key becomes meta_data.extracted_text_key")], "Derived output grant, write, and saved-key round trip") +
    '<p>The AI sends back the same key the backend supplied. The saved artifact points at that exact output. If the AI invents a separate bare key or the callback saves a rebuilt path, the record and stored object can disagree even when the upload itself succeeded.</p>' +
    predict('The backend returns a write link under Maharastra’s root. Should the AI prepend the deployment media root before uploading?', 'No. The signed link already names the destination and the backend’s returned key identifies it. Rewriting either breaks the agreement and can invalidate the signature.')),
section("contract", "Strict inputs make integration errors visible",
    '<p>The guide says unknown request fields produce a <strong>400 response naming the field</strong>. When adding a supported input, update the backend’s allowed-key contract deliberately. A field accepted by an AI client alone is not automatically accepted by the backend.</p>' +
    '<p>The AI’s <code>request_id</code> corresponds to the artifact’s backend <code>ai_request_id</code>. It is <strong>not</strong> the artifact row ID. Use the right identifier when correlating a callback with persisted data.</p>' +
    '<p>The guide found its account-specific storage defects on the backend side because the AI followed granted URLs. That is a finding from the reviewed branches, not a claim that AI integrations can never contain bugs. Verify the destination, callback key, and contract when investigating a new failure.</p>' + SNAPSHOT),
section("try", "Watch the full document handoff", lab("journey")),
], ["The backend chooses and signs case-data keys; the AI uses the returned links.", "READ_CASE_BUNDLE reads a ZIP; WRITE_DERIVED grants per-file output writes.", "Save the returned derived key exactly; AI request_id maps to ai_request_id, not the artifact ID."])

lesson("file-journey", "Follow one PDF from upload to AI output", 22,
    "Trace complaint.pdf through the browser, backend, Azure, AI service, and database. Then compare the lifecycle of other case files.",
    ["Describe all nine stages of the uploaded-PDF flow.", "Separate who decides a key from who uploads the bytes.", "Classify case files by routing and saved-versus-built behavior."], [
section("setup", "Give the story a concrete owner",
    '<p>In the guide’s worked example, case 9001 belongs to the customer <strong>Maharastra</strong>. Its media root is <code>crimeos-backend-maha-police-prod/mahapolice-prod/media</code>. We will follow one original PDF and the text derived from it. They are two blobs, with two saved references.</p>' +
    '<p>The account root is important, but it is only part of the full address. The selected Azure account and the reader’s configured container also have to agree. The browser exercise below uses fictional account names and sends no network requests.</p>'),
section("upload", "Stages 1–4: the original upload",
    flow([("1 · Officer selects", "complaint.pdf in the application"), ("2 · Backend prepares", "key_for_case builds an owner-rooted key; backend signs a write grant"), ("3 · Browser uploads", "The PDF bytes go directly to Azure through that grant"), ("4 · Backend records", "A CaseArtifact row saves the file URL")], "Original PDF: officer chooses, backend grants, browser uploads, backend saves reference") +
    '<p>“The backend decides the key” does not mean the PDF must travel through the backend. In the described flow, the browser transfers bytes directly to storage. The database stores the reference and metadata; the storage account stores the PDF.</p>' +
    code('Original key shape:\n<media root>/case-artifacts/9001/<upload-uuid>/complaint.pdf\n\nSaved reference:\ninvestigations_caseartifact.meta_data.file_url')),
section("derived", "Stages 5–9: AI-derived text",
    flow([("5 · AI gets read access", "A signed read link opens the original PDF"), ("6 · AI asks for output access", "WRITE_DERIVED requests names for this case and run"), ("7 · Backend returns", "Keys and write links under the same owner’s media root"), ("8 · AI writes and reports", "Text bytes go to Azure; the returned key goes back to the backend"), ("9 · Backend persists", "extracted_text_key records the derived blob")], "AI reads original, requests grant, writes derived text, and returns the exact key") +
    table(["Object", "Who chooses its key?", "Who writes its bytes?", "Saved member"], [
        ["Original complaint.pdf", "Backend using key_for_case", "Browser", '<code>meta_data.file_url</code>'],
        ["Derived complaint_pages_1-3.md", "Backend storage grants", "AI service", '<code>meta_data.extracted_text_key</code>'],
    ]) +
    '<p>Later reads use the saved derived key. Merely knowing the current case ID is not enough to reconstruct the original upload UUID or the AI run’s output name. The saved reference preserves that exact object identity.</p>'),
section("catalog", "Other files do not all have the same lifecycle",
    table(["File", "Routing in the guide", "Saved or built?", "Important behavior"], [
        ['Case bundle · <code>case_context_data/&lt;id&gt;.zip</code>', "Customer-rooted", "Built", '<code>case_ai_key</code>; backend rebuild workflow when no <code>CaseAIData</code> bundle exists'],
        ['<code>index.md</code>', "Customer-rooted; fixed 2026-11-05 in guide", "Built", "Rewritten from DB on artifact confirmation/discard; included in bundle ZIP"],
        ['Case memory · <code>Memory/MEMORY.txt</code>', "Customer-rooted", "Built", "Path uses unit, station, year, and police case number; not the DB case ID"],
        ["Case folder, chargesheet, case diary", "Customer-rooted", "Saved", "Folder paths use unit/station/year/number rather than DB case ID"],
        ["Case-document OCR text", "Bare key → deployment", "Saved", "Known hand-off item 1; do not assume dedicated storage configuration fixes it"],
        ["Evidence statement text", "Bare key → deployment", "Built", "Can be regenerated from DB; guide calls this lower priority"],
        ["Case-letter downloads", "Bare key → deployment", "Generated on download; saved if filed", "Filed copy depends on its saved blob; guide hand-off item 3"],
    ])),
section("observe", "Diagnose the stage, not just the filename",
    '<p>If upload succeeds but extraction fails, verify the AI’s read grant and the original object. If AI output upload succeeds but the app cannot show text, compare the callback key with <code>extracted_text_key</code>. If a bundle is stale, inspect the bundle/index publication workflow rather than renaming the original PDF.</p>' +
    predict('The original PDF opens, but its extracted text is missing after a migration. Does that prove storage access is correct for both?', 'No. They are distinct objects with distinct saved references. Inspect each exact key, its route, and whether its bytes were copied. The original being present does not recreate the derived text.') + SNAPSHOT),
section("try", "Advance the document one stage at a time", lab("journey")),
], ["The backend chooses keys, while the browser and AI can upload bytes directly with grants.", "Original and derived files have separate saved references.", "Use the file-type catalog before assuming that every missing file can be rebuilt."])

lesson("migration", "Move database records and files deliberately", 25,
    "See why copied rows do not carry PDF bytes, how keep_urls preserves old addresses, and why new IDs can break validators even when files exist.",
    ["Separate database migration from blob copying and routing configuration.", "Explain the MH tool’s keep_urls, storage origin, ID offset, and excluded bundle row.", "Predict missing files, successful reads, regeneration, and old-ID validation failures."], [
section("cards", "Moving the index does not move the cupboard",
    flow([("Database move", "Rows, fields, summaries, and saved path text"), ("Blob copy", "A separate operation transfers file bytes"), ("Destination configuration", "The saved root must select the account/container holding those bytes")], "Migration requires row transfer, blob transfer, and destination routing configuration") +
    '<p>Imagine an index card saying “file A is in cupboard C.” Copying that card gives you the address, not the file. In the same way, a database dump can contain <code>file_url</code> while containing none of the referenced PDF bytes.</p>' +
    table(["Item", "Moves with the described database tool?", "What to verify separately"], [
        ["Rows, fields, summaries", "Yes", "Relationships and transformed IDs"],
        ["Saved path text", "Yes; keep_urls preserves it", "Does the key still route correctly?"],
        ["Blob bytes", "No", "Copy existence, content, and destination coordinates"],
        ["Case DB ID", "Changes by an offset", "Built paths and validators using the current ID"],
    ])),
section("mh-tool", "The guide’s MH-to-demo migration contract",
    '<p>The guide describes branch <code>feature/demo/mh-final-migration-20261104</code> and tool directory <code>data_loading/mh_migration/</code>. Its default <code>keep_urls</code> behavior leaves saved paths unchanged. Referenced files are expected to be copied separately with <strong>identical keys</strong>.</p>' +
    '<p>For the MH customer in demo, the reviewed mapping sets prefix <code>crimeos-backend-maha-police-prod</code> and stage <code>mahapolice-prod</code>. A preserved key beginning with that root can then route through the customer’s configured storage connection. The mapping is recorded in <code>iam/constants/account_storage_origins.py</code>.</p>' +
    '<p>The tool excludes <code>cases.CaseAIData</code>. The destination therefore does not inherit a bundle row pointing at an old generated ZIP; the bundle-generation workflow can build one under the new case ID. This design is different from preserving an original upload’s saved key.</p>'),
section("outcomes", "Predict the result from all the conditions",
    table(["Situation", "Expected result in the described system", "Why"], [
        ["Preserved customer root, correct connection/container, object copied at exact key", "Found", "Address resolution and bytes agree"],
        ["Correct customer root but object not copied", "Missing", "A saved address does not regenerate bytes"],
        ["Bare key whose bytes remain only in another deployment’s account", "Missing in demo", "It routes to demo deployment storage"],
        ["Bare key and both deployments actually share the same container", "May be found", "The resolved coordinates may already address the same blob"],
        ["DB-ID-built bundle or index with available source data", "Regenerable under the new ID", "The corresponding generation workflow must run"],
        ["Saved old-ID path checked against a new-ID prefix", "Rejected even if object exists", "Validation and the stored address disagree"],
        ["Case-folder path based on unit/station/year/number", "DB-ID offset alone has no effect", "Its recipe does not contain the database ID"],
    ])),
section("id-example", "One old ID can still be a valid saved address",
    code('Before move:\n  Case ID: 214\n  Saved upload: delhi/prod/media/case-artifacts/214/run-1/a.pdf\n\nAfter move with keep_urls:\n  Case ID: 9001\n  Saved upload: delhi/prod/media/case-artifacts/214/run-1/a.pdf\n  Built bundle: delhi/prod/media/case_context_data/9001.zip\n\nWrong read-time guard:\n  require saved upload starts with .../case-artifacts/9001/') +
    '<p>The guide calls out intake, refund/defreeze, and draft-read checks that build a prefix from the current ID. Such a check can reject a valid preserved file. Do not “fix” it by constructing an address that was never written; inspect the persisted reference and ownership validation.</p>' +
    predict('Case 214 becomes 9001. The saved upload exists and routes correctly. Is the old 214 segment by itself evidence of a broken migration?', 'No. keep_urls intentionally preserves the saved object address. Check object existence, routing, and any validator. A built bundle can use 9001 while the preserved upload continues to use 214.')),
section("safe-copy", "A move must protect the source until verification",
    '<p>The guide found an application <code>move_object</code> path that could delete the source after an unverified or failed copy. Its rule is <strong>copy, verify completion and correctness, then delete</strong>. It recommends <code>copy_object_strict</code> rather than the error-hiding <code>copy_object</code> path.</p>' +
    '<p>Check the actual helper’s contract before using it in a new tool. A requested or accepted copy is not evidence that the destination bytes are complete. Do not turn a missing destination into loss of the only source copy.</p>' + SNAPSHOT),
section("try", "Move the records, bytes, and configuration separately", lab("migration")),
], ["keep_urls preserves path text, not blob bytes.", "Correct destination root, connection, container, and exact copied key must agree.", "Old-ID saved paths can remain valid; new-ID validators and bare-key fallback can still break them."])

lesson("rules", "Write file-handling code that preserves ownership", 25,
    "Turn the guide’s discovered mistakes into eleven implementation rules and a focused review checklist.",
    ["Recognize bare keys, rebuilt saved-path guards, unsafe moves, and wrong tool connections.", "Apply the eleven storage rules to a new case-file feature.", "Review writer, reader, validator, and migration behavior together."], [
section("mistakes", "Five mistake classes explain many failures",
    table(["Mistake", "What it looks like", "Consequence", "Guide examples"], [
        ["Bare key", '<code>"cases/{case_id}/..."</code> reaches storage without the media root', "Silently uses deployment storage", "OCR text, case letters; index.md was fixed"],
        ["Current-ID guard on saved address", '<code>path.startswith(...current_case_id...)</code>', "Rejects a preserved old-ID or old-root path", "Intake, refund/defreeze, draft reads"],
        ["Delete after unverified copy", "Move continues when a copy hides an error", "Can remove the only complete copy", "Data-bundle and CFCFRMS report moves"],
        ["Wrong tool connection", '<code>AZURE_CONNECTION_STRING</code> used directly for all files', "Misses customer storage", "Older case_migration tools and scripts"],
        ["Trusting the saved host", "Expecting an old full URL to select its old storage", "Wrong diagnosis after moving DB rows", "CrimeOS reader extracts only the key"],
    ])),
section("eleven", "Eleven rules for a new storage feature",
    '<ol>'
    '<li><strong>Start under the deployment media root, then route.</strong> Build a normal key under <code>settings.MEDIAFILES_LOCATION</code> and use the appropriate owner helper. Check that the returned key starts with the expected owner root.</li>'
    '<li><strong>Pick the helper by ownership.</strong> Use the case, actor, account, jurisdiction, or chat helper as appropriate. An intentionally deployment-wide object can stay bare, with a comment explaining that decision.</li>'
    '<li><strong>Choose saved or built explicitly.</strong> Persist the full returned key or URL for a saved file. A built file needs available inputs and a regeneration workflow.</li>'
    '<li><strong>Read a saved file from its saved value.</strong> Do not rebuild its address from current IDs. Validate ownership and stored references without assuming the historical name contains the current ID.</li>'
    '<li><strong>Keep writers, readers, and validators consistent.</strong> Use the same key-building contract where rebuilding is intended, and preserve compatibility with saved older paths.</li>'
    '<li><strong>Copy, verify, then delete.</strong> The guide recommends <code>copy_object_strict</code>; do not delete after the error-hiding copy path.</li>'
    '<li><strong>Route folder prefixes too.</strong> A list or delete prefix needs the full correct root. A short prefix can silently search deployment storage.</li>'
    '<li><strong>Keep AI storage behind grants.</strong> The AI chooses neither case-data keys nor storage credentials. Add a deliberate grants operation or supported payload field when needed.</li>'
    '<li><strong>Keep credentials out of logs.</strong> This includes connection strings, webhook secrets, and signed URLs.</li>'
    '<li><strong>Use the sanitiser’s filename.</strong> Raw names can contain traversal-shaped input such as <code>../</code>. Use the validated result when building the key.</li>'
    '<li><strong>Check customer-root routing in a meaningful test.</strong> Use a case whose owning customer has dedicated storage. The guide cites <code>test_index_key_follows_the_cases_owning_account</code> as an example.</li>'
    '</ol>'),
section("feature", "Worked feature: save a generated PDF",
    flow([("Resolve owner", "Use the case’s station and configured ownership fallback"), ("Build and route key", "MEDIAFILES_LOCATION plus sanitized filename; key_for_case"), ("Write and save", "Write bytes, then record the returned full address"), ("Read and verify", "Use the saved address; exercise old-ID and customer-storage cases")], "New saved-PDF feature: resolve owner, build key, persist address, read saved address") +
    code('Illustrative flow, not a drop-in production implementation:\n\nlegacy_key = <MEDIAFILES_LOCATION>/<kind>/<case_id>/<safe_filename>\nkey = key_for_case(case_id, legacy_key)\nwrite_file(key, pdf_bytes)\nsave_reference(key)\n\n# Later read:\nkey = read_saved_reference()\nread_file(key)', "Pseudocode · storage and persistence APIs depend on the feature") +
    '<p>Confirm successful storage before advertising a usable saved file. If a database update and blob write can fail independently, design how the feature detects and repairs incomplete work. The browser simulation does not claim to implement production transaction handling.</p>'),
section("review", "Six questions for the pull request",
    '<ul>'
    '<li>Does a new plain string reach <code>put_object</code>, <code>get_object</code>, or <code>generate_signed_*_url</code> without an owner helper?</li>'
    '<li>Is the address saved? If so, which table and column? If not, what can rebuild the file?</li>'
    '<li>Does a validator compare a saved address against a prefix built from the current ID?</li>'
    '<li>Does a copy or move verify the destination before deleting its source?</li>'
    '<li>Does a script bypass routing by using the deployment connection directly?</li>'
    '<li>Does the feature work both for a customer with dedicated storage and for one using deployment storage?</li>'
    '</ul>' +
    predict('A new list operation uses <code>case-artifacts/9001/</code>. It performs no writes. Can it still be wrong?', 'Yes. Prefixes are routed like keys. Without the correct owner media root, the list can inspect deployment storage and report no files even though the customer’s blobs exist.') + SNAPSHOT),
], ["A successful read/write pair can still put customer data in the wrong storage.", "Saved addresses, built-address recipes, and ownership checks need a consistent contract.", "Verify copies before deletion; route prefixes as carefully as full keys."])

lesson("debugging", "Debug “file not found” in a useful order", 22,
    "Gather the saved reference, compute the actual route, and inspect exact coordinates before changing IDs or copying files again.",
    ["Apply the guide’s six-step debugging order.", "Distinguish a missing object, wrong route, expired grant, and rejected validator.", "Read a scoped artifact-path query without exposing credentials."], [
section("six-steps", "Follow the evidence from reference to bytes",
    table(["Step", "Question", "Evidence to collect"], [
        ["1", "Is the file saved-path or built-path?", "The model column or the generating function; use the file catalog"],
        ["2", "What exact key is used?", "Saved key, or URL path after dropping the container; otherwise the actual built key"],
        ["3", "Which storage does this start select?", "Deployment-root match, customer-root match, or fallback"],
        ["4", "Is that exact object in that account and container?", "Inspect the resolved coordinates, not a similar name elsewhere"],
        ["5", "Does an old ID/root trigger a new-path guard?", "Reader/validator checks compared with the saved value"],
        ["6", "Is customer configuration current?", "Prefix, stage, connection configuration and the 60-second route cache"],
    ]) +
    flow([("Reference", "Saved field or generating recipe"), ("Key", "Exact full name"), ("Route", "Resolved account and container"), ("Object / guard", "Bytes exist? Request permitted? Validator accepts?")], "Debugging follows a reference to a key, route, and object rather than guessing from the visible URL") +
    '<p>Do not begin by renaming every blob that contains an old case ID. First determine whether the read is deliberately using a saved old-ID address and whether the request ever reaches storage.</p>'),
section("query", "Read-only example: inspect saved letter paths",
    code("SELECT case_id, system_entity_id, file_name,\n       meta_data::json ->> 'file_url' AS file_url\nFROM investigations_caseartifact\nWHERE system_entity_type = 'CASE_LETTER'\nORDER BY case_id DESC\nLIMIT 5;", "PostgreSQL read-only reference query · run only against an authorized database") +
    '<p>This query returns a few saved paths for filed letters. It does not inspect Azure, transfer files, repair references, or reveal the storage connection string. Confirm the real table, field types, and permissions before using it; these names come from the guide’s model inspection.</p>' +
    '<p>Paths may contain case information. Keep diagnostic output appropriately scoped. Never include signed query strings, account keys, or webhook secrets in a report.</p>'),
section("different-errors", "“Not found” is a symptom, not a complete diagnosis",
    table(["Evidence", "Likely question to investigate", "What not to assume"], [
        ["Object exists only in a different Azure account", "Did key routing choose a fallback or stale configuration?", "Matching filename means matching object"],
        ["Saved original exists but extracted output does not", "Was derived output copied and its returned key saved?", "Original access recreates extracted text"],
        ["Application rejects path before making a request", "Does a validator rebuild the current-ID prefix?", "Azure deleted the object"],
        ["Grant was valid earlier, access now fails", "Does the grant allow this operation and is it still valid?", "The object must be missing"],
        ["Customer setting was just changed", "Is the process still within the routing cache interval?", "The new setting has already been used everywhere"],
    ])),
section("worked", "Worked incident: OCR URL names alpha, demo cannot read it",
    '<p>Suppose the saved URL contains host <code>crimeosbackendalpha...</code> and path <code>private-files/cases/6453/ocr_results/a.txt</code>. The described helper extracts <code>cases/6453/ocr_results/a.txt</code>. Because that is bare, demo’s router chooses demo deployment storage.</p>' +
    '<p>Finding the file in alpha does not prove demo opened alpha. Compare the account and container actually selected in demo. If the deployments do not share the same container, the bytes must be made available through a deliberate copy/routing plan; changing the URL host alone does not change this helper’s route.</p>' +
    predict('The saved host is correct, but the key is bare. Will replacing only the host repair the described CrimeOS read?', 'No. That helper ignores the saved host. Determine the key’s route, destination container, and actual object existence. A repair must match the reader’s resolution contract.') + SNAPSHOT),
section("try", "Investigate simulated failures", lab("debugging")),
], ["Classify the reference, extract the key, resolve storage, and check that exact object.", "Check validators and cache before rewriting preserved addresses.", "A read-only SQL query returns references; it does not establish blob existence."])

lesson("code-map", "Know where each storage decision lives", 15,
    "Use the guide’s code map to find ownership, key construction, routing, grants, saved metadata, and migration behavior without searching blindly.",
    ["Pick the file that owns a particular storage responsibility.", "Trace a feature across owner lookup, key helper, adapter, and persisted reference.", "Use the guide’s limitations when planning a current-code investigation."], [
section("layers", "Read the feature through its layers",
    flow([("Feature / model", "What file is this and is its path saved?"), ("Ownership service", "Which customer owns it?"), ("Key helper + router", "Which name and storage connection?"), ("Azure adapter", "Read, write, sign, copy, list, or delete")], "Code navigation from feature and ownership through key routing to the storage adapter") +
    '<p>Begin with the failing operation. A broken customer-root key points toward helpers or ownership. A bad URL extraction points toward the URL utility. A correct key plus a bad signature points toward the adapter and selected credential. Following these boundaries keeps changes focused.</p>'),
section("map", "Backend and AI code map from the guide",
    table(["Responsibility", "Code location", "Look for"], [
        ["Key helpers and routing", '<code>common/utils/account_storage.py</code>', '<code>connection_for_key</code>, owner key helpers, cache and root matching'],
        ["Case/chat/user ownership", '<code>common/services/account_storage_routing.py</code><br><code>common/adapters/account_service_ownership.py</code>', "Station ownership and actor fallback"],
        ["Prefix configuration validation", '<code>common/utils/account_storage_config.py</code>', "Allowed and conflicting storage-root settings"],
        ["Storage operations", '<code>common/adapters/azure_storage_service.py</code>', "Reads, writes, signing, copy, move, delete"],
        ["Saved URL to key", '<code>common/utils/cloud_storage_utils.py</code>', '<code>get_object_key_from_file_url</code>'],
        ["Customer storage fields", '<code>iam</code> app · <code>Account</code> model', "Prefix, stage, encrypted connection string"],
        ["Reviewed migration origins", '<code>iam/constants/account_storage_origins.py</code>', "MH mapping and separate identical-key copy expectation"],
        ["Storage-grants endpoint", '<code>cases/views/get_case_storage_grants/</code><br><code>cases/interactors/ai_case/</code>', "Allowed request fields, operations, ownership, signing"],
        ["AI grants client", '<code>ai_platform/services/backend_storage/</code> in <code>crimeos-ai</code>', "Request grants, use returned URLs, return output keys"],
        ["Artifact persistence", '<code>investigations/models/case_artifact.py</code>', '<code>meta_data</code>, <code>file_path_hash</code>, request correlation'],
        ["Case-folder path construction", '<code>cases/interactors/get_case_folders.py</code>', "Unit, station, year, police case number"],
        ["Artifact index publication", '<code>investigations/interactors/artifacts/artifact_summary_publication.py</code>', '<code>index_object_key</code> and index rewrite workflow'],
        ["MH migration tool", '<code>data_loading/mh_migration/</code>', "keep_urls, ID offset, excluded CaseAIData"],
        ["Outstanding issue hand-off", '<code>account-storage-bare-key-handoff.html</code>', "Guide-era OCR, letter, validator, and move issues"],
    ])),
section("walkthrough", "Choose a starting point from the symptom",
    table(["Task", "Start here", "Then follow"], [
        ["New case-owned generated file", "Feature writer and model", "key_for_case → routing → adapter → saved-path reader"],
        ["AI output stored under the wrong customer", "WRITE_DERIVED interactor", "Owner lookup → returned key → selected signer → callback persistence"],
        ["Migration retains URL but read fails", "Saved field and URL-to-key helper", "Root mapping → destination object → old-ID validator"],
        ["Folder listing misses customer files", "Prefix-building call site", "Full media root → connection_for_key → list operation"],
    ]) +
    predict('A developer wants to understand why a saved full URL’s host does not affect routing. Which two code locations explain the behavior?', '<code>common/utils/cloud_storage_utils.py</code> explains URL-to-key extraction; <code>common/utils/account_storage.py</code> explains connection selection from that key.')),
section("limits", "Know what the guide did not inspect",
    '<p>The supplied guide does not cover the <code>scripts/</code> directory comprehensively, Odisha/Telangana schedule clients, or Azure network rules and CORS. It describes model-derived table names rather than a live schema. Its fixes and outstanding issue list belong to the reviewed branches and dates.</p>' +
    '<p>A current-code audit should record the exact checkout/commit, trace both writer and reader, inspect validators and migrations, and verify dedicated-customer plus deployment-storage behavior. The simulations teach the guide’s rules; they do not connect to the application repositories or prove a production configuration.</p>' +
    '<p>Use <a href="practice.html">the practice labs</a> to exercise the model, <a href="quiz.html">the explained quiz</a> to find gaps, and <a href="reference.html">the reference</a> for source links and a quick review.</p>' + SNAPSHOT),
], ["Find ownership in the service, key routing in account_storage.py, and I/O in the Azure adapter.", "Trace saved-path parsing and the reader’s route together.", "The code map is a dated guide snapshot; inspect current checkouts before making production claims."])

GLOSSARY = [
    dict(term="Azure storage account", meaning="A named Azure resource that holds storage data, including Blob containers. It is distinct from a CrimeOS customer Account.", example="lessonstore.blob.core.windows.net"),
    dict(term="Container", meaning="A collection of blobs inside one Azure storage account; it is one coordinate of an object’s address.", example="private-files"),
    dict(term="Blob", meaning="One stored object containing bytes and associated properties or metadata.", example="A PDF, a ZIP bundle, or an extracted Markdown file"),
    dict(term="Blob key / blob name", meaning="The full name of a blob inside its container. This is not the secret storage account access key.", example="delhi/prod/media/case-artifacts/214/run-1/a.pdf"),
    dict(term="Host / endpoint", meaning="The server address used to contact a storage service. The guide’s URL-to-key helper discards a saved host before making its own request.", example="lessonstore.blob.core.windows.net"),
    dict(term="Account access key / Shared Key", meaning="A broad storage account credential used for Shared Key authorization and account-key signing where enabled.", example="A secret value; never included in this course"),
    dict(term="Connection string", meaning="Connection settings. The guide uses a string containing an account name and account access key; other connection-string forms exist.", example="Stored in backend configuration or encrypted customer settings"),
    dict(term="SAS / signed link", meaning="A URL token granting access within a specified resource scope, permissions, and validity interval. It is a credential while usable.", example="A per-file write grant lasting about 300 seconds in the guide"),
    dict(term="Permission", meaning="An allowed operation, such as reading or writing. One permission does not imply all others.", example="A write-only grant cannot be used for a download"),
    dict(term="Expiry", meaning="The end of a grant’s validity interval; a fresh grant may be needed after that time.", example="Case-bundle read grants last about 900 seconds in the guide"),
    dict(term="Microsoft Entra ID", meaning="Azure identity authorization alternative to sharing a storage account key.", example="An identity authorized to obtain a user delegation key"),
    dict(term="Managed identity", meaning="An Azure-managed identity a supported application can use for identity-based access without storing an account access key.", example="An Azure-hosted backend identity with the required data access role"),
    dict(term="User delegation SAS", meaning="A SAS signed with a user delegation key obtained through Microsoft Entra authorization, instead of directly using the account access key.", example="An identity-based SAS option; not the signer described in the CrimeOS snapshot"),
    dict(term="Deployment", meaning="One running copy of the application with its own settings. Different deployments can still share an Azure account.", example="alpha, gamma, demo, staging, production"),
    dict(term="Customer Account", meaning="A CrimeOS customer organisation represented by the iam Account model.", example="The guide’s Maharastra customer"),
    dict(term="Deployment storage", meaning="The Azure connection and container configured for the running environment; also the described route fallback.", example="AZURE_CONNECTION_STRING and AZURE_PRIVATE_CONTAINER"),
    dict(term="Customer / account storage", meaning="Optional customer-specific storage described by a prefix, stage, and encrypted connection string.", example="Delhi’s prefix delhi and stage prod"),
    dict(term="Station / jurisdiction", meaning="The case’s station, used to find the owning customer account in the guide’s ownership flow.", example="Case → station → customer → storage configuration"),
    dict(term="Actor", meaning="The user performing an operation; the guide uses the actor’s account as an ownership fallback when needed.", example="The logged-in user when a case has no station"),
    dict(term="Prefix", meaning="The starting text of a blob name used for matching or grouping. A boundary slash prevents accidental neighboring-ID matches.", example="case-artifacts/214/"),
    dict(term="Stage root", meaning="The prefix/stage/ start used by the CrimeOS connection router.", example="delhi/prod/"),
    dict(term="Media root", meaning="The prefix/stage/media start of a normal CrimeOS storage key.", example="delhi/prod/media"),
    dict(term="MEDIAFILES_LOCATION", meaning="The deployment’s normal media root; owner helpers replace this expected start when routing customer-owned files.", example="crimeosbackend-demo/demo/media"),
    dict(term="Routed key", meaning="A key whose beginning matches the intended owner’s configured storage root.", example="delhi/prod/media/case_context_data/214.zip"),
    dict(term="Bare key", meaning="A key lacking a matching configured root; it falls back to deployment storage in the described configuration.", example="cases/214/ocr_results/a.txt"),
    dict(term="Routing", meaning="The application’s choice of storage connection from the key’s start: deployment root, customer root, or deployment fallback.", example="connection_for_key(key)"),
    dict(term="Routing cache", meaning="The described in-process cached list of storage origins, with a 60-second lifetime.", example="A just-edited account root may not be used immediately"),
    dict(term="Saved path", meaning="A full key or URL persisted when a file is created and read back as the file’s address.", example="CaseArtifact.meta_data.extracted_text_key"),
    dict(term="Built path", meaning="A key recomputed from identifiers or business fields rather than read from a saved object-address field.", example="An owner-rooted case_context_data/9001.zip"),
    dict(term="Virtual folder / flat namespace", meaning="A folder-like view produced by grouping blob names that share a prefix; slashes are characters in names.", example="Listing every name beginning case-artifacts/214/"),
    dict(term="Hierarchical namespace", meaning="An Azure Blob/Data Lake configuration supporting directory objects rather than only a flat naming view.", example="A broader Azure capability, not the guide’s virtual-folder model"),
    dict(term="CaseArtifact", meaning="The guide’s artifact model holding saved original/derived file metadata and request correlation fields.", example="investigations_caseartifact.meta_data.file_url"),
    dict(term="file_path_hash", meaning="An artifact lookup hash derived from a path; it is not the object key or the file bytes.", example="A hash on the CaseArtifact row"),
    dict(term="Storage grant", meaning="A backend response giving a permitted file key and signed access URL for a requested case operation.", example="READ_CASE_BUNDLE or WRITE_DERIVED"),
    dict(term="Derived file", meaning="Output computed from an original, such as extracted text. It is a separate blob with its own address.", example="complaint_pages_1-3.md"),
    dict(term="Case bundle", meaning="A generated ZIP that packages case context for the AI service.", example="<media root>/case_context_data/214.zip"),
    dict(term="keep_urls", meaning="The described migration mode preserving saved path text; it does not transfer referenced blob bytes.", example="Old-ID artifact URLs remain unchanged after an ID offset"),
    dict(term="ID offset", meaning="A transformation that adds an offset to database identifiers during the described migration.", example="A source case 214 becomes destination case 9001"),
    dict(term="Sanitiser", meaning="Code that validates or transforms untrusted filename input before it is used in a storage key.", example="Use its returned safe filename rather than raw ../ input"),
    dict(term="Verified move", meaning="Copy to the intended destination, verify completion/correctness, and delete the source only after success.", example="The guide recommends copy_object_strict before deletion"),
]

SOURCES = [
    dict(title="Supplied CrimeOS storage learning guide", url="reference.html#guide", description="Azure storage and how CrimeOS stores files, dated 2026-11-06. Source for application behavior and branch findings; not a new audit of current repositories."),
    dict(title="Introduction to Azure Blob Storage", url="https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction", description="Official resource model: storage accounts, containers, and blobs."),
    dict(title="Naming and referencing containers and blobs", url="https://learn.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata", description="Official naming and URI details, including flat and hierarchical namespace distinctions."),
    dict(title="Azure Data Lake Storage hierarchical namespace", url="https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-namespace", description="Directory objects and the qualification to the guide’s virtual-folder explanation."),
    dict(title="Shared access signature overview", url="https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview", description="SAS scope, permissions, validity, and supported SAS types."),
    dict(title="Manage storage account access keys", url="https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage", description="Account-key handling and Microsoft’s identity-based authorization guidance."),
    dict(title="Delegate access with a shared access signature", url="https://learn.microsoft.com/en-us/rest/api/storageservices/delegating-access-with-a-shared-access-signature", description="Official delegation model and authorization recommendations."),
]
