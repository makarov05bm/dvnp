// DVNP - Finding: h2c Upgrade Smuggling (Skyblue "internal-billing" microservice)
//
// This simulates a Go microservice that supports HTTP/2 cleartext (h2c)
// upgrades for internal low-latency communication -- a common, "sensible"
// choice for intra-network Go services, and rarely an out-of-the-box default,
// but easy to reach for since golang.org/x/net/http2/h2c makes it a one-liner.
//
// It has one endpoint that's meant to be reachable from outside (/) and one
// that's meant to be internal-only (/flag), with the access decision
// delegated entirely to the edge proxy (nginx) sitting in front of it.
package main

import (
	"fmt"
	"log"
	"net/http"

	"golang.org/x/net/http2"
	"golang.org/x/net/http2/h2c"
)

func main() {
	h2s := &http2.Server{}

	mux := http.NewServeMux()

	mux.HandleFunc("/billing", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "HOME - Skyblue internal-billing service. proto=%s path=%s\n", r.Proto, r.URL.Path)
	})

	// Meant to be reachable only from other internal services, never
	// directly from the internet. portal.skyblue.com enforces this with a
	// `location /billing/admin { deny all; }` block -- but that control
	// only exists at the HTTP layer, and h2c smuggling bypasses it entirely.
	// (nginx strips the /billing/ prefix via proxy_pass .../9999/, so this
	// is served here as plain /admin.)
	mux.HandleFunc("/billing/admin", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "ADMIN - Skyblue internal billing admin -- refund overrides, account impersonation.\nDVNP{h2c_upgrade_smuggling_bypasses_edge_acls}\n")
	})

	server := &http.Server{
		Addr: "0.0.0.0:9999",
		// h2c.NewHandler wraps the mux so the server accepts:
		//   1. Plain HTTP/1.1 requests, and
		//   2. HTTP/1.1 requests carrying `Upgrade: h2c`, which it will
		//      switch to full HTTP/2 semantics over the same TCP socket.
		Handler: h2c.NewHandler(mux, h2s),
	}

	log.Printf("Skyblue internal-billing service listening on :9999 (h2c-enabled)")
	log.Fatal(server.ListenAndServe())
}
