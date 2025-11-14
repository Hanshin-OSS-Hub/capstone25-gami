using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TalkManager : MonoBehaviour
{
    Dictionary<int, string[]> talkData;

    void Awake()
    {
        talkData = new Dictionary<int, string[]>();
        GenerateData();
    }

    void GenerateData()
    {
        talkData.Add(1001, new string[] { "한글 테스트" });
        talkData.Add(1002, new string[] { "Hello? I'm 1002" });
        talkData.Add(1003, new string[] { "Hello? 한글 테스팅" });
        talkData.Add(1004, new string[] { "Hello, World!" });
        talkData.Add(1005, new string[] { "테스트 세트" });
        talkData.Add(1006, new string[] { "투명 드래곤이 울부짖었따" });
    }

    public string GetTalk(int id, int talkIndex)
    {
        if (talkIndex == talkData[id].Length)
            return null;
        else
            return talkData[id][talkIndex];
    }
}
