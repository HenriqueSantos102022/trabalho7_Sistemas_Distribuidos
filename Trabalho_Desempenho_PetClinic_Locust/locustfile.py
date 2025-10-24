import random
import threading
from locust import HttpUser, task, between

class PetClinicUser(HttpUser):
    wait_time = between(0.5, 2.0)
    
    # Lista de IDs de proprietários (owners) que o Locust conhece.
    # Começa com os 10 padrão que vêm com a aplicação.
    owner_ids = list(range(1, 11))
    
    # Um 'lock' é necessário para que múltiplos usuários 
    # não tentem adicionar o mesmo ID ao mesmo tempo.
    owner_id_lock = threading.Lock()

    def on_start(self):
        """
        Executado uma vez por usuário virtual quando ele inicia.
        (Neste caso, não precisamos fazer nada, pois a lista de IDs é de classe)
        """
        pass

    # Tarefa 1: GET /owners (lista donos) - 40%
    @task(40)
    def get_owners_list(self):
        self.client.get("/api/customer/owners")

    # Tarefa 2: GET /owners/{id} - 30%
    @task(30)
    def get_owner_by_id(self):
        # Escolhe um ID aleatório DA LISTA de IDs conhecidos
        # (incluindo os que foram criados durante o teste)
        chosen_id = random.choice(PetClinicUser.owner_ids)
        
        self.client.get(
            f"/api/customer/owners/{chosen_id}",
            name="/api/customer/owners/[id]" # Agrupa URLs no Locust
        )

    # Tarefa 3: GET /vets - 20%
    @task(20)
    def get_vets_list(self):
        self.client.get("/api/vet/vets")

    # Tarefa 4: POST /owners (cadastro simples) - 10%
    @task(10)
    def create_owner(self):
        # Payload simples para criar um novo dono
        new_owner = {
            "firstName": "Usuario",
            "lastName": "TesteLocust",
            "address": "Rua do Teste, 123",
            "city": "Goiania",
            "telephone": "6299999999"
        }
        
        response = self.client.post("/api/customer/owners", json=new_owner)
        
        # Se o cadastro funcionou, adiciona o novo ID à lista
        if response.ok:
            try:
                new_owner_id = response.json().get("id")
                if new_owner_id:
                    # Usa o lock para adicionar o ID com segurança
                    with PetClinicUser.owner_id_lock:
                        if new_owner_id not in PetClinicUser.owner_ids:
                            PetClinicUser.owner_ids.append(new_owner_id)
            except Exception:
                # Ignora caso a resposta não seja um JSON válido
                pass