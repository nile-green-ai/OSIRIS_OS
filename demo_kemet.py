from modules.ra_fixed import RA
from modules.thoth import THOTH
from metrics.maat import MAAT
from agents.isis import ISIS
from agents.anubis import ANUBIS

def main():
    agent_id = "voidchi_prime"

    ra = RA(agent_id=agent_id)
    thoth = THOTH(agent_id=agent_id)
    maat = MAAT(agent_id=agent_id)
    isis = ISIS(agent_id=agent_id)
    anubis = ANUBIS(agent_id=agent_id)

    print("\n✅ Modules online:", [m.__class__.__name__ for m in [ra, thoth, maat, isis, anubis]])

    # RA
    if hasattr(ra, "activate"):
        r = ra.activate()
        print("\n🌞 RA.activate():", r)

    # THOTH
    if hasattr(thoth, "log_event"):
        thoth.log_event("DEMO_START", {"agent_id": agent_id})
        print("\n📜 THOTH logged DEMO_START")

    # MAAT
    if hasattr(maat, "check_balance"):
        ok = maat.check_balance({"energy": 1.0, "entropy": -1.0})
        print("\n⚖️ MAAT.check_balance():", ok)

    # ANUBIS
    if hasattr(anubis, "validate"):
        v = anubis.validate({"x": 1}, lambda x: isinstance(x, dict), context="demo")
        print("\n🐾 ANUBIS.validate():", v)

    # ISIS
    if hasattr(isis, "compile"):
        fragments = [{"a": 1}, {"b": 2}]
        expected = {"a": 0, "b": 0, "c": 0}
        out = isis.compile(fragments, expected)
        print("\n🌙 ISIS.compile():", out)

    print("\n🔥 Demo complete.")

if __name__ == "__main__":
    main()
