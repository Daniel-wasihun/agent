# 🌍 Optimal Search Strategies for Journey Planning from Big City to Benin 🌍

## ✨ Introduction

Four travelers embark on a unique journey, each with distinct information to guide them. **Person 1** seeks to hide in another city for 3 months, while **Persons 2, 3, and 4** aim to travel from **Big City** to **Benin**. Their information varies:

- **Person 1**: No information (no map, no distances).
- **Person 2**: Heuristic (estimated) distances via communication.
- **Person 3**: Actual distances via a city map.
- **Person 4**: Both heuristic and actual distances.

This document presents the best search strategies for each traveler, leveraging a graph of cities with actual and heuristic distances, to ensure efficient and effective journey planning.

## 🗺️ Graph and Data

The journey is modeled as a graph with **14 cities** and their connections:

### Cities
- Big City, Benghazi, Petra, Kinshasa, Giza, Lagos, Varanasi, Larnaca, Luxor, Cadiz, Cairo, Ife, Benin, Addis Ababa

### Connections (Actual Distances)
- Big City → Benghazi: 100
- Big City → Petra: 140
- Big City → Kinshasa: 90
- Big City → Giza: 330
- Big City → Lagos: 98
- Big City → Varanasi: 670
- Benghazi → Larnaca: 60
- Benghazi → Luxor: 420
- Petra → Luxor: 210
- Petra → Cadiz: 200
- Kinshasa → Giza: 320
- Kinshasa → Cairo: 420
- Giza → Ife: 360
- Giza → Benin: 90
- Lagos → Addis Ababa: 120
- Cairo → Ife: 90
- Ife → Benin: 90
- Addis Ababa → Benin: 110

### Heuristic Values (Estimated Distances to Benin)
- Big City: 500
- Benghazi: 600
- Petra: 600
- Kinshasa: 400
- Giza: 200
- Lagos: 400
- Varanasi: 1000
- Larnaca: 900
- Luxor: 700
- Cadiz: 800
- Cairo: 600
- Ife: 400
- Benin: 0
- Addis Ababa: 200

**Start**: Big City  
**Goal for Persons 2, 3, 4**: Benin  
**Goal for Person 1**: Hide in another city for 3 months

## 🚶 Search Strategies and Results

### 🕵️‍♂️ Person 1: Hiding Strategy
- **Information**: None (no map, no distances, no heuristics).
- **Goal**: Hide in another city for 3 months.
- **Strategy**: Random selection or blind search (Breadth-First Search [BFS] or Depth-First Search [DFS]).
- **Recommendation**: Travel to a nearby city like **Kinshasa (90 units)** or **Lagos (98 units)** to hide. No goal-directed search is needed.
- **Analysis**: Without information, a simple move to a nearby city minimizes travel exposure. The provided BFS/DFS solution (Big City → Giza → Benin, cost 420, BFS: 15 nodes, DFS: 13 nodes) incorrectly assumes a goal of reaching Benin.
  - **BFS**:
    - Expanded nodes: Big City(0), Benghazi(100), Petra(140), Kinshasa(90), Giza(330), Lagos(98), Varanasi(670), Larnaca(160), Luxor(520), Luxor(350), Cadiz(340), Cairo(510), Giza(410), Ife(690), Benin(420), Addis Ababa(218)
    - Path: Big City → Giza → Benin, cost 420
    - Nodes expanded: 15
  - **DFS**:
    - Expanded nodes: Big City(0), Benghazi(100), Larnaca(160), Luxor(520), Petra(140), Luxor(350), Cadiz(340), Kinshasa(90), Cairo(510), Ife(510), Giza(410), Giza(330), Benin(420)
    - Path: Big City → Giza → Benin, cost 420
    - Nodes expanded: 13
- **Rationale**: Random selection of a nearby city is sufficient for hiding.

### 🌐 Person 2: Greedy Best-First Search
- **Information**: Heuristic distances only.
- **Goal**: Reach Benin from Big City.
- **Strategy**: Greedy Best-First Search (selects node with lowest heuristic value, h(n)).
- **Result**: Path **Big City → Giza → Benin**, cost **420** (330 + 90), **3 nodes expanded**.
  - **Steps**:
    - Node tested 0, expanded 0:
      - Expanded node: Big City(500)
      - Open list: Big City(500)
    - Node tested 1, expanded 1:
      - Expanded node: Big City(500)
      - Open list: Giza(200), Kinshasa(400), Lagos(400), Benghazi(600), Petra(600), Varanasi(1000)
    - Node tested 2, expanded 2:
      - Expanded node: Big City(500), Giza(200)
      - Open list: Benin(0), Ife(400), Kinshasa(400), Lagos(400), Benghazi(600), Petra(600), Varanasi(1000)
    - Node tested 3, expanded 2:
      - Expanded node: Big City(500), Giza(200), Benin(0)
      - Open list: Ife(400), Kinshasa(400), Lagos(400), Benghazi(600), Petra(600), Varanasi(1000)
- **Analysis**: Fast but suboptimal, as the optimal path is Big City → Lagos → Addis Ababa → Benin (cost 328).
- **Recommendation**: Use Greedy search for quick results when only heuristic data is available.

### 🗺️ Person 3: Uniform Cost Search (UCS)
- **Information**: Actual distances only.
- **Goal**: Reach Benin from Big City.
- **Strategy**: UCS (expands node with lowest cumulative path cost, g(n)).
- **Result**: Path **Big City → Lagos → Addis Ababa → Benin**, cost **328** (98 + 120 + 110), **8 nodes expanded**.
  - **Steps**:
    - Expanded node: Big City(0)
      - Node list: Kinshasa(90), Lagos(98), Benghazi(100), Petra(140), Giza(330), Varanasi(670)
    - Expanded node: Kinshasa(90)
      - Node list: Lagos(98), Benghazi(100), Petra(140), Giza(330), Giza(410), Cairo(510), Varanasi(670)
    - Expanded node: Lagos(98)
      - Node list: Benghazi(100), Petra(140), Addis Ababa(218), Giza(330), Giza(410), Cairo(510), Varanasi(670)
    - Expanded node: Benghazi(100)
      - Node list: Petra(140), Larnaca(160), Addis Ababa(218), Giza(330), Giza(410), Cairo(510), Luxor(520), Varanasi(670)
    - Expanded node: Petra(140)
      - Node list: Larnaca(160), Addis Ababa(218), Giza(330), Luxor(350), Luxor(340), Cadiz(340), Giza(410), Cairo(510), Luxor(520), Varanasi(670)
    - Expanded node: Larnaca(160)
      - Node list: Addis Ababa(218), Giza(330), Luxor(350), Luxor(340), Cadiz(340), Giza(410), Cairo(510), Luxor(520), Varanasi(670)
    - Expanded node: Addis Ababa(218)
      - Node list: Benin(328), Giza(330), Luxor(350), Luxor(340), Cadiz(340), Giza(410), Cairo(510), Luxor(520), Varanasi(670)
    - Expanded node: Benin(328)
      - Node list: Giza(330), Luxor(350), Luxor(340), Cadiz(340), Giza(410), Cairo(510), Luxor(520), Varanasi(670)
- **Analysis**: Guarantees the shortest path by prioritizing actual costs.
- **Recommendation**: Use UCS for optimal results with actual distances.

### 🌟 Person 4: A* Search
- **Information**: Both heuristic and actual distances.
- **Goal**: Reach Benin from Big City.
- **Strategy**: A* Search (minimizes f(n) = g(n) + h(n), where g(n) is actual cost and h(n) is heuristic estimate).
- **Result**: Path **Big City → Lagos → Addis Ababa → Benin**, cost **328**, **5 nodes expanded**.
  - **Steps**:
    - Expanded node: Big City(500)
      - Node list: Kinshasa(490), Lagos(498), Giza(530), Benghazi(700), Petra(740), Varanasi(1670)
    - Expanded node: Kinshasa(490)
      - Node list: Lagos(498), Giza(530), Giza(610), Benghazi(700), Petra(740), Cairo(1110), Varanasi(1670)
    - Expanded node: Lagos(498)
      - Node list: Addis Ababa(418), Giza(530), Giza(610), Benghazi(700), Petra(740), Cairo(1110), Varanasi(1670)
    - Expanded node: Addis Ababa(418)
      - Node list: Benin(328), Giza(530), Giza(610), Benghazi(700), Petra(740), Cairo(1110), Varanasi(1670)
    - Expanded node: Benin(328)
      - Node list: Giza(530), Giza(610), Benghazi(700), Petra(740), Cairo(1110), Varanasi(1670)
  - **A* Table**:
    | City       | g(n)       | h(n) | f(n) = g(n) + h(n) | h*(n) |
    |------------|------------|------|--------------------|-------|
    | Big City   | 0          | 500  | 500                | 328   |
    | Benghazi   | 100        | 600  | 700                | 428   |
    | Petra      | 140        | 600  | 740                | 388   |
    | Kinshasa   | 90         | 400  | 490                | 410   |
    | Giza       | 330/410    | 200  | 530/610            | 170   |
    | Lagos      | 98         | 400  | 498                | 402   |
    | Varanasi   | 670        | 1000 | 1670               | 0     |
    | Larnaca    | 160        | 900  | 1060               | 168   |
    | Luxor      | 520/350    | 700  | 1220/1050          | 148   |
    | Cadiz      | 340        | 800  | 1140               | 160   |
    | Cairo      | 510        | 600  | 1110               | 0     |
    | Ife        | 510/690    | 400  | 910/1090           | 0     |
    | Benin      | 500/420/328| 0    | 500/420/328        | 0     |
    | Addis Ababa| 218        | 200  | 418                | 110   |
- **Analysis**: Optimal and efficient, expanding fewer nodes than UCS due to heuristic guidance.
- **Recommendation**: Use A* for the best balance of efficiency and optimality when both data types are available.

## 📊 Comparison of Strategies

| **Person** | **Information** | **Strategy** | **Path** | **Cost** | **Nodes Expanded** | **Optimal?** |
|------------|-----------------|--------------|----------|----------|--------------------|--------------|
| 1          | None            | Random/BFS   | Kinshasa or Lagos | 90 or 98 | Varies | N/A (hiding) |
| 2          | Heuristic       | Greedy       | Big City → Giza → Benin | 420 | 3 | No |
| 3          | Actual          | UCS          | Big City → Lagos → Addis Ababa → Benin | 328 | 8 | Yes |
| 4          | Both            | A*           | Big City → Lagos → Addis Ababa → Benin | 328 | 5 | Yes |

### 📈 Search Efficiency Chart
The chart below compares the number of nodes expanded by each search strategy for Persons 2, 3, and 4, highlighting A*’s efficiency.

```chartjs
{
  "type": "bar",
  "data": {
    "labels": ["Greedy (Person 2)", "UCS (Person 3)", "A* (Person 4)"],
    "datasets": [{
      "label": "Nodes Expanded",
      "data": [3, 8, 5],
      "backgroundColor": ["#36A2EB", "#FF6384", "#4BC0C0"],
      "borderColor": ["#2A8BBF", "#CC4F67", "#3B9C9C"],
      "borderWidth": 1
    }]
  },
  "options": {
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": {
          "display": true,
          "text": "Nodes Expanded"
        }
      },
      "x": {
        "title": {
          "display": true,
          "text": "Search Strategy"
        }
      }
    },
    "plugins": {
      "title": {
        "display": true,
        "text": "Search Efficiency Comparison"
      }
    }
  }
}
```

## 🏁 Conclusion

- **Person 1**: Move to **Kinshasa** or **Lagos** for hiding, as no specific destination is required.
- **Person 2**: Greedy search is fast but yields a suboptimal path (cost 420 vs. 328).
- **Person 3**: UCS ensures the optimal path (Big City → Lagos → Addis Ababa → Benin, cost 328).
- **Person 4**: A* provides the optimal path with fewer nodes expanded, making it the most efficient.

**Key Insight**: A* is ideal when both heuristic and actual distances are available, while UCS guarantees optimality with only actual distances. For hiding, a nearby city suffices.

## 🌟 Recommendations

- **For Person 1**: Provide basic distance information to nearby cities to optimize hiding.
- **For Person 2**: Supplement heuristic data with actual distances for better pathfinding.
- **For All**: Use A* whenever both data types are available for the best balance of efficiency and optimality.

