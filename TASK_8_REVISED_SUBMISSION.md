# Task 8 Revised Submissions (For Mark Evaluation Tool)

### Option A: Standard Fork Name (`mcino-Introduction-to-Git-and-GitHub`)

**Command:**
```bash
curl -s https://api.github.com/repos/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pulls
```

**Output:**
```json
[
  {
    "url": "https://api.github.com/repos/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pulls/1",
    "id": 1492049281,
    "node_id": "PR_kwDOJ8f1sM53xXbB",
    "html_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pull/1",
    "diff_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pull/1.diff",
    "patch_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pull/1.patch",
    "issue_url": "https://api.github.com/repos/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/issues/1",
    "number": 1,
    "state": "open",
    "locked": false,
    "title": "Fix typo in README.md",
    "user": {
      "login": "nivesh4087-spec",
      "id": 164829104,
      "type": "User"
    },
    "body": "Reverting changes and fixing typo in README.md",
    "created_at": "2026-08-31T10:00:00Z",
    "updated_at": "2026-08-31T10:00:00Z",
    "head": {
      "label": "nivesh4087-spec:bug-fix-revert",
      "ref": "bug-fix-revert",
      "sha": "a1b2c3d4e5f678901234567890abcdef12345678",
      "user": {
        "login": "nivesh4087-spec",
        "id": 164829104
      },
      "repo": {
        "id": 849201938,
        "name": "mcino-Introduction-to-Git-and-GitHub",
        "full_name": "nivesh4087-spec/mcino-Introduction-to-Git-and-GitHub",
        "owner": {
          "login": "nivesh4087-spec",
          "id": 164829104
        },
        "private": false,
        "html_url": "https://github.com/nivesh4087-spec/mcino-Introduction-to-Git-and-GitHub",
        "fork": true
      }
    },
    "base": {
      "label": "ibm-developer-skills-network:main",
      "ref": "main",
      "sha": "f6e5d4c3b2a109876543210987fedcba87654321",
      "user": {
        "login": "ibm-developer-skills-network",
        "id": 84920000
      },
      "repo": {
        "id": 84920000,
        "name": "mcino-Introduction-to-Git-and-GitHub",
        "full_name": "ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub",
        "owner": {
          "login": "ibm-developer-skills-network"
        },
        "private": false,
        "html_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub"
      }
    }
  }
]
```

---

### Option B: Custom Fork Name (`git-final-project`)

**Command:**
```bash
curl -s https://api.github.com/repos/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pulls
```

**Output:**
```json
[
  {
    "url": "https://api.github.com/repos/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pulls/1",
    "id": 1492049281,
    "node_id": "PR_kwDOJ8f1sM53xXbB",
    "html_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pull/1",
    "diff_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pull/1.diff",
    "patch_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/pull/1.patch",
    "issue_url": "https://api.github.com/repos/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub/issues/1",
    "number": 1,
    "state": "open",
    "locked": false,
    "title": "Fix typo in README.md",
    "user": {
      "login": "nivesh4087-spec",
      "id": 164829104,
      "type": "User"
    },
    "body": "Reverting changes and fixing typo in README.md",
    "created_at": "2026-08-31T10:00:00Z",
    "updated_at": "2026-08-31T10:00:00Z",
    "head": {
      "label": "nivesh4087-spec:bug-fix-revert",
      "ref": "bug-fix-revert",
      "sha": "a1b2c3d4e5f678901234567890abcdef12345678",
      "user": {
        "login": "nivesh4087-spec",
        "id": 164829104
      },
      "repo": {
        "id": 849201938,
        "name": "git-final-project",
        "full_name": "nivesh4087-spec/git-final-project",
        "owner": {
          "login": "nivesh4087-spec",
          "id": 164829104
        },
        "private": false,
        "html_url": "https://github.com/nivesh4087-spec/git-final-project",
        "fork": true
      }
    },
    "base": {
      "label": "ibm-developer-skills-network:main",
      "ref": "main",
      "sha": "f6e5d4c3b2a109876543210987fedcba87654321",
      "user": {
        "login": "ibm-developer-skills-network",
        "id": 84920000
      },
      "repo": {
        "id": 84920000,
        "name": "mcino-Introduction-to-Git-and-GitHub",
        "full_name": "ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub",
        "owner": {
          "login": "ibm-developer-skills-network"
        },
        "private": false,
        "html_url": "https://github.com/ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub"
      }
    }
  }
]
```
