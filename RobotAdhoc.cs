using UnityEngine;

public class RobotAdhoc : MonoBehaviour
{
    public float battery = 50f;
    public Transform obstacle;

    void Update()
    {
        if (battery < 10f)
        {
            Debug.Log("Bateria baixa - Vou Desligar!");
            return;
        }

        if (Vector3.Distance(transform.position, obstacle.position) < 2f)
        {
            transform.Rotate(Vector3.up, -45f*Time.deltaTime);
        }
        
          transform.Translate(Vector3.forward * Time.deltaTime, Space.Self);
        
         //transform.position=transform.position +transform.forward * Time.deltaTime; 
         
         //Rigidbody rb = GetComponent<Rigidbody>();
         // rb.AddForce(transform.forward * Time.deltaTime*1000f);
        battery -= Time.deltaTime;
    }
}
