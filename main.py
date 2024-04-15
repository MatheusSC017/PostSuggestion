from core.post import PostSuggest

if __name__ == "__main__":
    post_suggest = PostSuggest()

    # Drone 20x20cms, com capacidade de voo de até 100 metro de altitude, bateria com duração de 15 minutos, kit acompanhado 3 baterias, equipamento de manutenção, helices reservas e equipamentos de limpeza
    # Adicione ênfase a altitude de voo e adicione a informação sobre uma promoção com duração de 1 uma única semana
    # Adicione ênfase a capacidade da bateria e adicione a informação sobre uma promoção com duração de 1 um único dia
    # The product is on sale until the weekend, pay attention to the durability of the product and the good reviews received

    option = 0
    while option != 4:
        try:
            print("Choice an option:\n"
                  "1 - Get suggestions to post;\n"
                  "2 - Improve a suggested post;\n"
                  "3 - Translate a suggested post;\n"
                  "4 - Close;")
            option = int(input())

            if option == 1:
                print("Enter with the product/service characteristics: ")
                product = input()
                suggestions = post_suggest.get_suggestion(product_characteristics=product)
                for suggestion in suggestions:
                    print(f"\n{suggestion}")
            elif option == 2:
                print("Enter with the index of the suggestion: ")
                product = int(input())
                print("Enter with the adjustments requireds: ")
                adjustments = input()
                print(post_suggest.adjustment(1, adjustments))

            print("\n\n")

        except ValueError:
            print("Enter with a valid option!")
