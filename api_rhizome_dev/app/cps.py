from api_rhizome_dev.app.icx import Icx


class Cps(Icx):
    CPS_CONTRACT = "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f"

    def __init__(self) -> None:
        super().__init__()

    def get_project_count(self):
        result = self.call(self.CPS_CONTRACT, "get_project_amounts", {})
        for key in result.keys():
            result[key]["_count"] = int(result[key]["_count"], 16)
            for token in ["ICX", "bnUSD"]:
                result[key]["_total_amount"][token] = (
                    int(result[key]["_total_amount"][token], 16) / 10**18
                )
        return result

    def get_prep_count(self):
        result = self.call(self.CPS_CONTRACT, "get_PReps", {})
        return len(result)
