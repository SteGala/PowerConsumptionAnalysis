import infrastructure as infra

if __name__ == "__main__":
    infrastructure = infra.Infrastructure()
    print(infrastructure)
    infrastructure.schedule_wokloads(infra.compare_by_consumption)