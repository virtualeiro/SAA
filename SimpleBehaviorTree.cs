
using UnityEngine;

public class SimpleBehaviorTree : MonoBehaviour
{
    public float battery = 100f;
    public Transform enemy;

    void Update()
    {
        if (CheckEnemy() && Attack()) return;
        if (CheckBattery() && Recharge()) return;
        Explore();

        battery -= Time.deltaTime * 2;
    }

    bool CheckEnemy() => Vector3.Distance(transform.position, enemy.position) < 3f;
    bool CheckBattery() => battery < 20f;

    bool Attack() { Debug.Log("Atacar inimigo!"); return true; }
    bool Recharge() { Debug.Log("Recarregar..."); return true; }
    void Explore() { Debug.Log("Explorar área..."); }
}

/********************************************/
// RFA - Removed 
/********************************************/
/*
using UnityEngine;

public class SimpleBehaviorTree : MonoBehaviour
{
    public float battery = 100f;
    public Transform enemy;
    public float wanderSpeed = 2f;
    public float jumpForce = 0.5f;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        if (rb == null)
        {
            rb = gameObject.AddComponent<Rigidbody>();
        }
    }

    void Update()
    {
        if (CheckEnemy() && Attack()) return;
        if (CheckBattery() && Recharge()) return;
        Explore();

        battery -= Time.deltaTime * 2;
    }

    bool CheckEnemy() => Vector3.Distance(transform.position, enemy.position) < 3f;
    bool CheckBattery() => battery < 20f;

    bool Attack()
    {
        Debug.Log("Atacar inimigo!");
        if (IsGrounded())
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
        return true;
    }

    bool Recharge()
    {
        Debug.Log("Recarregar...");
        // Stop 
        rb.velocity = Vector3.zero;
        return true;
    }

    void Explore()
    {
        Debug.Log("Explorar área...");
        // Wander 
        rb.MovePosition(transform.position + transform.forward * wanderSpeed * Time.deltaTime);
    }

    bool IsGrounded()
    {
        // Ground check
        return Physics.Raycast(transform.position, Vector3.down, 1.1f);
    }
}

*/