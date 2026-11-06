"""Scenario questions with explanations for every option.

Application answers refer to the supplied CrimeOS guide dated 2026-11-06.
"""

QUESTIONS = []


def question(topic, prompt, answers, correct):
    QUESTIONS.append(dict(id="azure-q" + str(len(QUESTIONS) + 1).zfill(2), topic=topic, prompt=prompt,
                          options=[dict(text=text, why=why) for text, why in answers], correct=correct))


question("foundations", "Two Azure storage accounts each contain private-files/cases/214/a.pdf. Are these the same stored object?", [
    ("Yes, because the container and key match.", "The account is also part of the object’s coordinates. Matching container and key in different accounts still means separate blobs."),
    ("No. The complete coordinates include the storage account.", "A blob is identified by the account, container, and exact key together. Different accounts contain independent objects."),
    ("Only if the database case IDs match.", "A database ID does not merge Azure objects. It may be part of a blob name, but the account and container remain necessary."),
], 1)

question("foundations", "In the guide’s flat namespace, what does case-artifacts/214/run-1/a.md represent?", [
    ("One blob name containing slash characters.", "The folder view groups names by prefixes. It does not imply directory objects in a flat namespace."),
    ("Four real directories that Azure must create before upload.", "This is the flat-namespace model. Hierarchical namespace is a separate Azure capability with directory objects."),
    ("A signed access grant.", "This is only a name. A SAS token supplies authorization details; a blob key alone is not a signed grant."),
], 0)

question("foundations", "You want to list files for case 214 without matching case 2140. Which prefix is more precise?", [
    ("case-artifacts/214", "This text is also the start of case-artifacts/2140/. Use the trailing boundary slash for this naming convention."),
    ("case-artifacts/214/", "The slash separates the case-ID segment. In real CrimeOS code also include and route the complete owner media root."),
    ("214", "That omits both the file-kind and root boundaries and does not identify the intended case prefix."),
], 1)

question("access", "The AI has a valid write-only SAS for derived/a.md. Can it download original.pdf with that grant?", [
    ("Yes, because both files belong to one case.", "Case membership is not the grant’s resource scope. The original PDF is a different object and reading is a different operation."),
    ("Yes, while the link is unexpired.", "Time is only one condition. Resource scope and permissions must also allow the requested access."),
    ("No. The resource and requested operation are outside that grant.", "A write grant for one derived file does not authorize reading another blob. Request the appropriate backend grant."),
], 2)

question("access", "Why does the described AI service receive signed URLs instead of the account-key connection string?", [
    ("The account-key connection string can give broad account access; grants can be narrowly scoped and temporary.", "The backend retains the broad credential and delegates only the case-file operation the AI needs."),
    ("A connection string is only a longer form of the same per-file permission.", "An account-key connection string contains a broad secret. It is not equivalent to a narrow expiring file grant."),
    ("Azure never allows a service to use a connection string.", "Services can use supported credentials. The guide’s boundary deliberately prevents the AI from holding this broad one."),
], 0)

question("access", "A five-minute read link is used ten minutes after it was issued. What is the useful next action?", [
    ("Rename the blob so the signature becomes valid again.", "Renaming does not extend a token’s validity and would change the addressed resource."),
    ("Request a fresh authorized read grant through the backend.", "The original grant has expired. A fresh grant must still be for the correct resource and permitted operation."),
    ("Give the AI the account access key permanently.", "Broad credentials are not required to renew a narrow file grant and would break the described boundary."),
], 1)

question("access", "Which statement correctly qualifies the guide’s simplified SAS explanation?", [
    ("Every Azure SAS must allow exactly one action on exactly one blob.", "That describes the application’s narrow grants, not all Azure SAS capabilities. SAS resource scope and permissions are configurable."),
    ("Signed links never need to be treated as credentials because they expire.", "A valid bearer can use the granted access until it ends. Do not log or expose signed links."),
    ("Azure SAS can have broader scopes and multiple permissions; the guide intentionally uses narrow grants.", "Keep the general Azure capability separate from this application’s chosen defaults and account-key signer."),
], 2)

question("ownership", "A Delhi user opens a case whose station belongs to Maharastra. Which customer owns a new file for that case?", [
    ("Delhi, because the logged-in user always owns new files.", "The actor is a fallback when case ownership cannot be found through the station, not an override of an existing owner."),
    ("Maharastra, through the case’s station ownership.", "The guide follows case → station → customer. The viewing user does not become the case’s owner."),
    ("Whichever customer’s prefix appears alphabetically first.", "Owner selection is not alphabetical. It follows the described domain ownership relationships."),
], 1)

question("ownership", "A case has no station, but the actor has a known customer account. What does the guide describe?", [
    ("Use the actor’s customer account as the ownership fallback.", "This is the next fallback in the described owner-resolution service. If neither owner nor actor account can be found, it warns and uses deployment storage."),
    ("Read the old URL host to choose a customer.", "A saved host is not the ownership source in this flow, and the URL-to-key reader discards it."),
    ("Choose an arbitrary configured customer storage account.", "Arbitrary selection would mix ownership. The guide specifies actor fallback, then warned deployment fallback."),
], 0)

question("ownership", "The guide reports alpha and gamma sharing an Azure account and container. What can happen if both write cases/214/ocr_results/a.txt?", [
    ("Nothing; the STAGE setting automatically inserts a prefix into every string.", "The router does not automatically rewrite arbitrary bare keys. Their missing environment prefix is the defect."),
    ("Azure creates a hidden folder for each running application.", "Azure addresses the blob using its account, container, and supplied name. It does not add deployment ownership to a bare name."),
    ("They can address the same blob and an overwrite-enabled write can replace it.", "The coordinates are identical. Environment prefixes separate names only when the code actually uses those prefixes."),
], 2)

question("keys", "A case belongs to a customer with dedicated storage, but its saved key is cases/214/ocr_results/a.txt. Where does the described router read it?", [
    ("The customer’s storage, because the case ID is present.", "connection_for_key does not infer ownership from the middle case-ID segment. It matches the start of the key."),
    ("Deployment storage, because this bare start matches no configured root.", "This is the guide’s silent fallback. Customer settings do not repair an already bare key."),
    ("Every customer storage account at once.", "The normal connection router selects a connection. Searching candidates under every root is a separate helper use."),
], 1)

question("keys", "Which match has first priority in connection_for_key according to the guide?", [
    ("The deployment’s own prefix/stage root.", "Own deployment-root matching is checked first, followed by customer-root matching, then deployment fallback."),
    ("The customer whose name matches a file’s extension.", "File extensions do not select account ownership or storage connections."),
    ("The old host saved in the URL.", "The described URL helper drops that host before connection routing. The key’s start drives routing."),
], 0)

question("keys", "Demo has a customer root acme/prod/, but a saved key starts mh-prefix/prod/media/. What happens if no other root matches?", [
    ("The router substitutes acme/prod/ because the case now belongs to Acme.", "Connection selection does not rewrite a saved unmatched key into the current owner’s root."),
    ("The router always raises an exception for an unknown root.", "The guide describes a silent deployment fallback when nothing matches, not an unknown-root exception."),
    ("The router silently uses the deployment connection.", "Only configured matching starts select customer storage. A root-looking string is not enough if it is unknown."),
], 2)

question("keys", "What does key_for_case do with an input that does not start with MEDIAFILES_LOCATION in the guide?", [
    ("It always prepends the owner’s root.", "The helper swaps an expected deployment-media-root start. It is not a general bare-key repair function."),
    ("It leaves the input unchanged.", "This is why calling the helper with cases/214/a.txt can leave the bare-key defect intact. Build the normal rooted input first."),
    ("It signs a read URL for the input.", "Key construction is separate from signing. The helper returns a name; the adapter signs or accesses it later."),
], 1)

question("keys", "A profile picture belongs to a user rather than a case. Which helper fits the ownership?", [
    ("key_for_actor(user_id, legacy)", "This helper resolves the user’s customer. The helper should match who owns the file."),
    ("case_ai_key(case_id)", "That helper names a case context bundle ZIP, not a user-owned profile picture."),
    ("key_under_every_account(legacy)", "That helper generates search candidates when the owner is unknown. A known user owner should be routed directly."),
], 0)

question("keys", "Two customer accounts claim the same root with different connection strings. What behavior does the guide report?", [
    ("The router picks the most recently created customer silently.", "That is not the described conflict behavior. The configuration is ambiguous and should be corrected."),
    ("The router writes every file into both accounts.", "There is no described replication behavior here. Routing conflict does not imply copying to both destinations."),
    ("It logs an error and uses the deployment connection.", "This fallback can put files somewhere unexpected. Unique, correctly configured origins matter."),
], 2)

question("keys", "A customer root was changed seconds ago, but a process still uses old routing. What guide detail should be checked?", [
    ("The case PDF’s page count.", "Page count is unrelated to the cached mapping from key roots to connections."),
    ("The 60-second routing-list cache.", "A configuration edit may not be reflected immediately in an already cached process. Confirm the actual root and cache state."),
    ("Whether the customer name contains a space.", "The relevant routing inputs are configured prefix/stage and connection, not the display name alone."),
], 1)

question("paths", "A saved URL names crimeosbackendalpha.blob.core.windows.net. Does that saved host choose storage in the guide’s CrimeOS reader?", [
    ("No. The helper extracts the key and the current environment routes its start.", "The saved container is removed too. The reader uses its configured container. This is application behavior, not how a direct URL request works."),
    ("Yes. Every CrimeOS read must contact the saved host directly.", "The described code parses the saved value and sends its own routed request rather than opening that full URL directly."),
    ("Only if the key ends in .pdf.", "File type does not change the described host-dropping and key-routing behavior."),
], 0)

question("paths", "Where does the guide say the artifact’s AI-extracted text address is saved?", [
    ("In file_path_hash, as the original complete URL.", "file_path_hash is a lookup hash derived from a key. It is not the object address."),
    ("Only inside the AI service’s connection string.", "The AI does not hold that case-data connection string in the described design, and the backend persists the output reference."),
    ("CaseArtifact.meta_data.extracted_text_key.", "The backend saves the returned derived key in that metadata member so later reads use the same object address."),
], 2)

question("paths", "Case 214 becomes 9001. Its saved upload still points to an existing old-ID object, and routing is correct. What should a normal read use?", [
    ("A newly guessed key containing 9001.", "That may identify an object that was never written. Saved paths preserve exact historical addresses."),
    ("The saved old-ID address, subject to valid ownership and access checks.", "The old number in a blob name does not make the address invalid. Inspect validators that incorrectly require the new ID."),
    ("The file_path_hash as a signed URL.", "The lookup hash is neither the key nor a SAS token. It cannot be used as the object’s URL."),
], 1)

question("paths", "A missing file has a built path. Does that guarantee it instantly comes back on every read?", [
    ("No. A supported generation workflow still needs to run with the required source data.", "Built describes how its name is obtained. Regeneration is application behavior, not automatic Azure behavior."),
    ("Yes. Azure regenerates any blob whose filename includes a case ID.", "Azure does not read application database rows to regenerate absent files."),
    ("No built-path file can ever be recreated.", "The guide’s bundles, index, and evidence statement are examples with database-driven regeneration paths."),
], 0)

question("backend-ai", "Which grant operation returns one owner-rooted key and write URL per requested output filename?", [
    ("READ_CASE_BUNDLE", "That operation grants read access to a generated case context ZIP, not per-file output writes."),
    ("A direct AI request using AZURE_STORAGE_CONNECTION_STRING", "The described AI case-data flow uses backend grants rather than holding the storage account credential."),
    ("WRITE_DERIVED", "Its payload includes run_id and file_names. The backend resolves ownership and returns destinations under that owner’s media root."),
], 2)

question("backend-ai", "After uploading derived text with the granted URL, which key should the AI return?", [
    ("The exact key returned by the backend grant.", "That key identifies the object written through the signed URL and is persisted as extracted_text_key."),
    ("A fresh bare key reconstructed from the current case ID.", "That can point the artifact at a different location from the successful upload and bypass customer routing."),
    ("The storage account access key.", "That is a secret credential, not an object identifier. The AI should not hold or return it."),
], 0)

question("backend-ai", "The AI adds an unsupported request field to the grants body. What response does the guide describe?", [
    ("The backend automatically stores it as an artifact field.", "Unknown grant fields are not automatically persisted. The request contract is deliberately restricted."),
    ("A 400 response naming the unknown field.", "A new supported input requires a deliberate update to the backend’s allowed-key contract."),
    ("A new storage account is created for the field.", "Grant validation does not provision customer storage accounts from arbitrary fields."),
], 1)

question("backend-ai", "The AI callback includes request_id. Which backend field does the guide say it corresponds to?", [
    ("The artifact row’s primary ID in all cases.", "The guide explicitly distinguishes the AI request identifier from the artifact identifier."),
    ("The station’s storage_prefix.", "A storage prefix is a routing configuration value, not a request correlation identifier."),
    ("The artifact’s ai_request_id.", "Use ai_request_id to correlate the AI request as described; do not substitute the artifact ID."),
], 2)

question("file-journey", "In the original-PDF upload flow, who chooses the key and who uploads the PDF bytes?", [
    ("The backend chooses the key; the browser uploads directly using its write grant.", "The service deciding the destination can be different from the client transferring the bytes."),
    ("The browser chooses any storage root; the AI uploads the original.", "The described backend resolves ownership and signs the permitted destination before the browser transfers the original."),
    ("The database stores the PDF bytes inside file_url.", "file_url stores a reference. Azure holds the blob bytes separately."),
], 0)

question("file-journey", "Which identifiers does the guide use in case-folder and case-memory naming instead of the database case ID?", [
    ("The current viewer’s user ID only.", "Viewing a case does not define its owning station or the business identifiers used for its folder."),
    ("Unit, station, year, and police case number.", "An offset to the database ID alone does not change those path inputs. Routing and those business values still matter."),
    ("The artifact’s signed URL expiry time.", "Grant expiry controls authorization time, not the stable business identity of a case folder."),
], 1)

question("file-journey", "What event does the guide associate with rewriting the artifact index.md?", [
    ("Every Azure container rename.", "The described workflow is tied to artifact publication state, not an Azure container rename."),
    ("Only a user changing their profile picture.", "Profile uploads are a different ownership flow and do not define case artifact-index publication."),
    ("Artifact confirmation or discard; the generated index is also shipped inside the bundle.", "The guide describes database-driven index publication and reports its customer-root fix dated 2026-11-05."),
], 2)

question("migration", "Database rows move to demo with keep_urls, but no blobs are copied. Which statement is accurate?", [
    ("Saved uploads and derived files reappear because their URL text was copied.", "Copied references do not contain blob bytes. Saved-only objects remain unavailable unless the resolved storage already has them."),
    ("Regenerable outputs can be rebuilt by their workflows; saved-only files do not return from path text alone.", "The guide lists bundles, index, and evidence statements among regenerable outputs. A generated screen-download letter differs from a saved filed copy."),
    ("Every missing object is permanently unrecoverable.", "Available source data or separate source blobs may support regeneration or copying. Inspect the file type and source availability."),
], 1)

question("migration", "What does keep_urls mean in the described MH tool?", [
    ("Saved paths stay unchanged; blob copying must be handled separately with matching keys.", "The mode preserves text references. The destination root/connection/container and copied objects must still align."),
    ("Every file is downloaded and embedded inside the database dump.", "The guide explicitly separates the file bytes from database transfer."),
    ("The destination must always use the old saved URL host directly.", "The described reader extracts and routes the key rather than trusting that saved host."),
], 0)

question("migration", "Why does the guide’s MH migration exclude cases.CaseAIData?", [
    ("To make the AI permanently unable to read the case.", "The exclusion supports rebuilding context in the destination; it is not a permanent access ban."),
    ("To delete all original uploaded PDFs.", "CaseAIData is the generated bundle state discussed here. It is not a command to delete saved originals."),
    ("So the destination bundle workflow can rebuild a ZIP under the new case ID.", "The destination does not inherit the old generated bundle row. Its rebuilt bundle can use the transformed ID."),
], 2)

question("migration", "Case 214 becomes 9001. What is the expected behavior of a case-folder file, an existing saved artifact, and a regenerable bundle when all other conditions are correct?", [
    ("All three must keep using the database ID 214 forever.", "The case folder uses business fields, the saved artifact keeps its old address, and the rebuilt bundle can use the new DB ID."),
    ("The folder path is unaffected by the DB-ID offset; the saved artifact can keep its old address; the bundle can be rebuilt under 9001.", "These different address strategies can all work. A guard rebuilding the saved artifact prefix from 9001 is a separate failure risk."),
    ("All three must be renamed to include 9001 before any read.", "That invents a uniform rule for files with different path strategies and can break valid saved references."),
], 1)

question("migration", "A saved old-ID artifact exists, but the application rejects it before Azure is contacted. What should you inspect?", [
    ("A validator comparing the saved path with a prefix built from the current case ID.", "The guide reports this class of intake, refund/defreeze, and draft-read failures. Existence alone does not bypass a faulty guard."),
    ("Only the Azure account’s displayed friendly name.", "The application has rejected the path before contacting Azure; inspect the code that made that decision."),
    ("Whether the PDF extension is lowercase.", "The stated evidence points to pre-storage validation. Inspect the actual guard before guessing about the filename."),
], 0)

question("rules", "You add a generated case PDF that must be saved. Which implementation follows the guide?", [
    ("Build cases/<id>/a.pdf directly and reconstruct it on every read.", "That is bare and also discards saved-address semantics. It can use deployment storage and fail after ID changes."),
    ("Let the AI decide a customer connection string and keep it.", "The backend owns routing and credentials in the described design; the AI uses narrow grants."),
    ("Build under MEDIAFILES_LOCATION, use key_for_case, write it, save the returned address, and read that saved value.", "Also verify the root for a case with dedicated customer storage and keep reader/validator behavior consistent."),
], 2)

question("rules", "What was wrong with the guide’s reviewed move_object path?", [
    ("It refused to copy any object under a customer root.", "The reported defect was failure handling: deleting the source even when a copy had not succeeded."),
    ("It could delete the source after an unverified or failed copy.", "The guide recommends a strict copy path with verified completion/correctness before deletion, protecting the only copy."),
    ("It required a blob name, which Azure does not use.", "Blob names are necessary object coordinates. The issue concerns copy verification and deletion order."),
], 1)

question("rules", "A script lists customer files using only AZURE_CONNECTION_STRING and a short prefix. Why can it miss data?", [
    ("It bypasses customer routing and can search only deployment storage with the wrong prefix.", "Listing needs the correct owner-rooted prefix and selected connection just like reading a full key."),
    ("Read-only lists always search every Azure account automatically.", "A list request is scoped to the connection and container used. Azure does not search all customer credentials for the script."),
    ("Customer files cannot be listed under any circumstances.", "They can be listed through authorized operations using the correct account, container, and prefix."),
], 0)

question("rules", "A raw filename contains ../. What should new key-building code use?", [
    ("The raw filename, because all slash-shaped input is automatically safe.", "The guide requires using the sanitiser’s returned filename; untrusted path-shaped input must not define unintended key structure."),
    ("The account access key in place of the filename.", "That would expose a secret and does not sanitize user input."),
    ("The filename returned by the application’s validation/sanitisation step.", "Use that validated result when constructing the rooted key. Do not validate one value and then accidentally store the raw one."),
], 2)

question("debugging", "What should the first debugging step establish for a missing file?", [
    ("Whether the object is addressed by a saved path or by a built path.", "That tells you where to obtain its actual key and whether a generation workflow may help."),
    ("Whether every database ID can be changed to match the old path.", "Changing IDs before understanding the address strategy can damage data and is not the guide’s diagnostic order."),
    ("Whether all customer credentials can be printed into a support log.", "Never print those secrets. Inspect authorized, scoped configuration and the route without exposing credentials."),
], 0)

question("debugging", "A SQL query returns meta_data.file_url for a filed letter. What has it proved?", [
    ("The blob exists and its signed link is unexpired.", "The query only reads persisted reference text. It does not inspect Azure object existence or validate a grant."),
    ("The row contains a saved reference; storage existence and routing still need checking.", "Continue by extracting the key, resolving the account/container, and checking that exact object."),
    ("The file was copied during keep_urls migration.", "keep_urls preserves text. A row with a URL does not prove the referenced bytes were transferred."),
], 1)

question("code-map", "Which pair explains how a saved full URL becomes a routed storage request?", [
    ("The browser theme toggle and course progress store.", "Those are learning-site functions and do not implement application blob routing."),
    ("The artifact filename extension and the AI model name.", "Neither selects the described URL-parsing and storage-origin functions."),
    ("cloud_storage_utils.py for URL-to-key extraction, then account_storage.py for connection routing.", "Trace parsing and routing together. The adapter subsequently performs the authorized I/O operation."),
], 2)

question("code-map", "Does completing these simulations prove the current production code and Azure configuration match the guide?", [
    ("No. They teach the dated guide model; current behavior requires inspecting the relevant checkout and configuration.", "The course labels source provenance, branch-specific findings, and the limits of its browser-only simulations."),
    ("Yes. The browser secretly tests every production customer account.", "The exercises use no credentials or application network requests and do not inspect production storage."),
    ("Yes, because all source guides remain correct after every deployment.", "Application behavior can change. Record the actual version and verify current writer/reader/validator paths for real work."),
], 0)
