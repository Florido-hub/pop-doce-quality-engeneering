def preparar_input_avaliacao(caso):
    if "turnos" in caso:
        turnos = [
            turno["entrada"]
            for turno in caso["turnos"]
        ]

        historico = "\n".join(
            f"Turno {i + 1}: {entrada}"
            for i, entrada in enumerate(turnos[:-1])
        )

        if not historico:
            return turnos[-1]

        return (
            f"Histórico da conversa:\n{historico}\n\n"
            f"Solicitação atual:\n{turnos[-1]}"
        )

    return caso["entrada"]
