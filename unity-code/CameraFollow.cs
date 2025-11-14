using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;  // 따라갈 대상 (플레이어)
    public float smoothSpeed = 5f;  // 따라오는 속도
    public Vector3 offset = new Vector3(0, 0, -10f);  // 거리 조정용 오프셋

    void LateUpdate()
    {
        if (target == null)
            return;

        Vector3 desiredPosition = target.position + offset;
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed * Time.deltaTime);
        transform.position = smoothedPosition;
    }
}