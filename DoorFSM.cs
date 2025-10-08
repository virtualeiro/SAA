using UnityEngine;

public class DoorFSM : MonoBehaviour
{
    enum State { Fechada, Abrindo, Aberta, Fechando }
    State current = State.Fechada;
    float timer = 0f;

    public Vector3 closedPosition;
    public Vector3 openPosition;
    public float moveSpeed = 2f;

    void Start()
    {
        closedPosition = transform.position;
        openPosition = closedPosition + Vector3.up * 3f; 
    }

    void Update()
    {
        timer += Time.deltaTime;

        switch (current)
        {
            case State.Fechada:
     //RFA           MoveDoor(closedPosition);
                if (Input.GetKeyDown(KeyCode.Space))
                    ChangeState(State.Abrindo);
                break;
            case State.Abrindo:
    //RFA            if (MoveDoor(openPosition))
                    if (timer > 1f) ChangeState(State.Aberta);
                break;
            case State.Aberta:
    //RFA            MoveDoor(openPosition);
                if (timer > 3f) ChangeState(State.Fechando);
                break;
            case State.Fechando:
    //RFA            if (MoveDoor(closedPosition))
                    if (timer > 1f) ChangeState(State.Fechada);
                break;
        }
    }

    bool MoveDoor(Vector3 target)
    {
        transform.position = Vector3.MoveTowards(transform.position, target, moveSpeed * Time.deltaTime);
        return Vector3.Distance(transform.position, target) < 0.01f;
    }

    void ChangeState(State newState)
    {
        current = newState;
        timer = 0f;
        Debug.Log("Porta agora: " + current);
    }
}
