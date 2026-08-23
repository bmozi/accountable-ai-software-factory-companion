# Executable Policy Example

[`default-policy.json`](default-policy.json) is the deterministic admission
floor used by the runnable journey. It limits work classes, authority modes,
environments, delegation, cost, and required prohibitions.

The policy is intentionally small. It demonstrates that a prompt does not
grant authority and that changing a Work Order cannot silently exceed the
admitted work-class contract. Replace it with an approved policy system and
locally legitimate rules before operational use.
