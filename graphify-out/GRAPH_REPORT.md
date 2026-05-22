# Graph Report - /Users/diwakarpatel/Documents/ragaai/deepagents-project  (2026-05-22)

## Corpus Check
- 15 files · ~4,930 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 81 nodes · 115 edges · 23 communities detected
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]

## God Nodes (most connected - your core abstractions)
1. `_service_path()` - 13 edges
2. `_run()` - 11 edges
3. `get_conn()` - 8 edges
4. `update_run()` - 5 edges
5. `get_run()` - 5 edges
6. `git_diff()` - 5 edges
7. `reject_run()` - 5 edges
8. `save_event()` - 4 edges
9. `search_service()` - 4 edges
10. `compile_java_service()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `_run()` --calls--> `run()`  [INFERRED]
  /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/agent.py → /Users/diwakarpatel/Documents/ragaai/deepagents-project/main.py
- `stream_run()` --calls--> `get_run()`  [INFERRED]
  /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/main.py → /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/db.py
- `get_diff()` --calls--> `get_run()`  [INFERRED]
  /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/main.py → /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/db.py
- `get_diff()` --calls--> `run()`  [INFERRED]
  /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/main.py → /Users/diwakarpatel/Documents/ragaai/deepagents-project/main.py
- `startup()` --calls--> `init_db()`  [INFERRED]
  /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/main.py → /Users/diwakarpatel/Documents/ragaai/deepagents-project/backend/db.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.21
Nodes (17): build_agent(), create_run(), get_conn(), get_events(), get_run(), get_runs(), init_db(), save_event() (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.2
Nodes (8): git_diff(), Show git diff (staged + unstaged) for a service repo., get_diff(), list_project_files(), List all files in the clinicalops-setup project., Read a file from the clinicalops-setup project. Path is relative to the project, read_project_file(), run()

### Community 2 - "Community 2"
Cohesion: 0.29
Nodes (9): edit_service_file(), list_service_files(), Create or overwrite a file in a service. path is relative to service root., Make a targeted string replacement in a service file., List files in a service. service: auth|gateway|internal-api|workflow|document|db, Read a file from a service. path is relative to the service root., read_service_file(), _service_path() (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.4
Nodes (5): git_push(), Run uv sync for an RPA to validate Python dependencies., Push current branch to remote in a service repo., _run(), sync_rpa()

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (4): BaseModel, ApproveRequest, RejectRequest, RunRequest

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (0): 

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (0): 

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (0): 

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (2): fetch_prd(), Fetch a PRD from a Google Docs or Notion URL, or return text as-is if not a URL.

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (2): git_create_branch(), Create a new git branch in a service repo.

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (2): git_commit(), Stage all changes and commit in a service repo.

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (2): git_status(), Show git status for a service repo.

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (2): compile_java_service(), Compile a Java service to validate changes. Returns PASS or FAIL with output.

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (2): create_pr(), Create a GitHub PR for a service repo using gh CLI.

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (2): Search for a string in a service. file_type: java|py|sql|yml|xml|properties, search_service()

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **16 isolated node(s):** `List all files in the clinicalops-setup project.`, `Read a file from the clinicalops-setup project. Path is relative to the project`, `Fetch a PRD from a Google Docs or Notion URL, or return text as-is if not a URL.`, `List files in a service. service: auth|gateway|internal-api|workflow|document|db`, `Read a file from a service. path is relative to the service root.` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 7`** (2 nodes): `RootLayout()`, `layout.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (2 nodes): `handleSubmit()`, `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (2 nodes): `parseDiff()`, `DiffViewer.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `fetch_prd()`, `Fetch a PRD from a Google Docs or Notion URL, or return text as-is if not a URL.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `git_create_branch()`, `Create a new git branch in a service repo.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `git_commit()`, `Stage all changes and commit in a service repo.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `git_status()`, `Show git status for a service repo.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (2 nodes): `compile_java_service()`, `Compile a Java service to validate changes. Returns PASS or FAIL with output.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `create_pr()`, `Create a GitHub PR for a service repo using gh CLI.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `Search for a string in a service. file_type: java|py|sql|yml|xml|properties`, `search_service()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `postcss.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `next-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `next.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `TestResults.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_diff()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.202) - this node is a cross-community bridge._
- **Why does `git_diff()` connect `Community 1` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `run()` connect `Community 1` to `Community 3`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `update_run()` (e.g. with `_run_agent()` and `reject_run()`) actually correct?**
  _`update_run()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `get_run()` (e.g. with `stream_run()` and `reject_run()`) actually correct?**
  _`get_run()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `List all files in the clinicalops-setup project.`, `Read a file from the clinicalops-setup project. Path is relative to the project`, `Fetch a PRD from a Google Docs or Notion URL, or return text as-is if not a URL.` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._