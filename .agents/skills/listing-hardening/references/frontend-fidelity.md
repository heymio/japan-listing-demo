# Frontend fidelity

## Purpose

Hardening verifies that a claimed channel-native Demo follows current consumer-facing evidence rather than an invented generic ecommerce shell.

## Evidence layers

Keep separate:

1. Platform Capability evidence — what the channel/account supports.
2. Frontend Visual evidence — how the current consumer-facing page actually looks and behaves.
3. Project Content evidence — approved assets/copy placed into verified editable regions.

Official rules do not substitute for current Frontend Visual evidence.

## Primary Reference

Use the Planning-owned **Primary Reference** and Channel Frontend Reference Pack. A secondary reference may fill an explicit gap but may not silently replace the Primary Reference.

## FRONTEND_FIDELITY_GATE

Immediately before native Demo Assembly, verify:

- current shell and material section order are visually supported;
- brand-controlled and platform-controlled regions are distinguished;
- material desktop structure is known;
- material mobile/app-web behavior is known or explicitly scoped out;
- planned interactions are evidenced by the locked reference/capability state;
- project content is inserted only into verified brand-controlled/demo regions;
- unsupported platform UI is not fabricated as product truth.

If these conditions are not met, do not label the deliverable channel-native.

## Content Review Demo fallback

When `FRONTEND_FIDELITY_GATE` cannot pass, produce a clearly named **Content Review Demo** if a review artifact is still useful. It may present approved content sequence and assets, but it must not fabricate marketplace chrome, buy-box behavior, tabs, cards, navigation, or other native UI and present them as verified.

## Stage 9 assembly

When fidelity is acceptable:

1. reproduce the verified shell/order first;
2. preserve evidenced hierarchy and interactions;
3. insert final-consumable project assets only into verified regions;
4. represent channel-owned regions conservatively;
5. keep internal status labels in Review Mode only;
6. ensure Review Mode overlays do not alter the underlying Consumer Mode layout.

The target is verified channel fidelity, not an original web-design interpretation.
