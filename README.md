# RustyBunny

This is a prototype of a very simple Remote Access Trojan (RAT) complete with C2C nodes that the RAT can dynamically switch between for instructions.

I'm implementing the initial version of this project in Python for ease of prototyping, but I will be porting it to Rust later on for speed and smaller executable size.

The latest version implements basic communications between a control node and its client_node. Roadmap for upcoming features:
- Bidirectional communication, returning client node results back to control node.
- Using subprocess to move comms channels to separate processes.
- Building out a system of channels in order to support things like downloads running in the background, multiple shell sessions, etc.
- Logic for the client node to search out known locations (forums, social media sites, etc) for live control nodes.
- Public key encryption for verifying the authenticity of nodes and establishing secure communications with them.
- Interactive shell support over the wire.
- Over the wire updates to the clien_node code, could be done in a modular way.
