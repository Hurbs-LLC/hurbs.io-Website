# TODO

- [ ] Blog search via Cloudflare AI Search (formerly AutoRAG)
  - Create an AI Search instance indexing hurbs.io (or the blog content in R2)
  - Add a small Worker API route for queries (deliberate exception to the
    static-assets-only rule; document in CLAUDE.md when built)
  - Brand-styled "Search the blog" box on /blog/ that understands natural
    language ("my wifi doesn't reach the back office")
  - Route the model calls through Cloudflare AI Gateway for caching,
    rate limiting, logging, and cost visibility
