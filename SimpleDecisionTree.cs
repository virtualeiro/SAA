using UnityEngine;

public class SimpleDecisionTree : MonoBehaviour
{
    public float battery = 100f;
    public Transform enemy;

    void Update()
    {
        if (battery < 20f)
        {
            Recharge();
        }
        else if (Vector3.Distance(transform.position, enemy.position) < 3f)
        {
            Attack();
        }
        else
        {
            Patrol();
        }

        battery -= Time.deltaTime * 2;
    }

    void Recharge() => Debug.Log("Recarregar...");
    void Attack() => Debug.Log("Atacar!");
    void Patrol() => Debug.Log("Patrulhar...");
}
