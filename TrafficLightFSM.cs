using UnityEngine;

public class TrafficLightFSM : MonoBehaviour
{
    enum State { Verde, Amarelo, Vermelho }
    State current = State.Verde;
    float timer = 0f;
    public GameObject luzVerde;
    public GameObject luzAmarela;
    public GameObject luzVermelha;



    void Update()
    {
        timer += Time.deltaTime;

        switch (current)
        {
            case State.Verde:
                if (timer > 5f) ChangeState(State.Amarelo);
                break;
            case State.Amarelo:
                if (timer > 2f) ChangeState(State.Vermelho);
                break;
            case State.Vermelho:
                if (timer > 5f) ChangeState(State.Verde);
                break;
        }
    }

    void ChangeState(State newState)
    {
        current = newState;
        timer = 0f;
        Debug.Log("Novo estado: " + current);
        Debug.Log("Tempo no estado: " + timer);
        UpdateLights();
    }

    void UpdateLights()
    {
        luzVerde.SetActive(current == State.Verde);
        luzAmarela.SetActive(current == State.Amarelo);
        luzVermelha.SetActive(current == State.Vermelho);

    }
}
