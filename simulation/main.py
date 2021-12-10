import infrastructure as infra

if __name__ == "__main__":
    infrastructure = infra.Infrastructure()

    print()
    print("Scheduling simulation optimized for power consumption")
    infrastructure.schedule_wokloads(infra.compare_by_consumption)

    print()
    print("Scheduling simulation optimized for execution score")
    infrastructure.schedule_wokloads(infra.compare_by_score)

    print()
    print("Scheduling simulation optimized for efficiency")
    infrastructure.schedule_wokloads(infra.compare_by_efficiency)