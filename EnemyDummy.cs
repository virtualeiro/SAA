using UnityEngine;

public class EnemyDummy : MonoBehaviour
{
    Vector3 hook;
    void Start()
    {
        hook = transform.position;
    }
    void Update()
    {
        transform.position = hook+new Vector3(Mathf.Sin(Time.time) * 1.3f, 0, Mathf.Cos(Time.time) * 1.3f);
    }
}
