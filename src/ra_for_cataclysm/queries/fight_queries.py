FETCH_SINGLE_FIGHT_WITH_EVENTS = """
query FetchSingleFightWithEvents($reportCode: String!, $fightID: Int!) {
  reportData {
    report(code: $reportCode) {
      code
      title
      fights(fightIDs: [$fightID]) {
        id
        name
        difficulty
        encounterID
        startTime
        endTime
        averageItemLevel
        bossPercentage
        fightPercentage
        lastPhase
        kill
        size
        completeRaid
        enemyPlayers
        friendlyPlayers
        gameZone {
          id
          name
        }
        enemyNPCs {
          id
          gameID
          instanceCount
        }
        dungeonPulls {
          startTime
          endTime
          enemyNPCs {
            id
            gameID
          }
        }
        maps {
          id
        }
      }
      events(fightIDs: [$fightID], limit: 10000) {
        data
        nextPageTimestamp
      }
    }
  }
}
"""
