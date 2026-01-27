from core.osiris_os import OSIRIS_OS


def main():
    osiris = OSIRIS_OS(
        agent_id="pm_demo_001",
        agent_name="Nova"
    )

    if hasattr(osiris, "boot"):
        osiris.boot()
    else:
        print("OSIRIS_OS initialized")

    if hasattr(osiris, "status"):
        print(osiris.status())


if __name__ == "__main__":
    main()

