import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { LineupsService } from '../_services/lineups.service';

interface LineupSizeOption {
  value: number;
  label: string;
}

interface LineupPlayer {
  player_id: string;
  name: string;
}

interface Lineup {
  players: LineupPlayer[];
  total_possessions: number;
  offensive_points: number;
  defensive_points: number;
  offensive_fg_pct: number;
  defensive_fg_pct: number;
  offensive_efg_pct: number;
  defensive_efg_pct: number;
  offensive_assists: number;
  offensive_turnovers: number;
  total_rebounds: number;
  offensive_rating: number;
  defensive_rating: number;
  net_rating: number;
  point_differential: number;
}

@Component({
  selector: 'lineups-summary-response-component',
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
  ],
  templateUrl: './lineups-summary-response.component.html',
  styleUrl: './lineups-summary-response.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LineupsSummaryResponseComponent implements OnInit {
  private readonly lineupsService = inject(LineupsService);
  private readonly cdr = inject(ChangeDetectorRef);

  readonly lineupSizes: LineupSizeOption[] = [
    { value: 5, label: '5 players' },
    { value: 4, label: '4 players' },
    { value: 3, label: '3 players' },
    { value: 2, label: '2 players' },
    { value: 1, label: '1 player' },
  ];

  leagueLineupSize = 5;

  lineups: Lineup[] = [];
  filteredLineups: Lineup[] = [];
  paginatedLineups: Lineup[] = [];
  topLineups: Lineup[] = [];

  searchTerm = '';

  sortColumn: keyof Lineup = 'net_rating';
  sortAscending = false;

  loading = false;
  errorMessage = '';

  readonly pageSize = 25;
  currentPage = 1;
  totalPages = 1;

  ngOnInit(): void {
    this.fetchLeagueApiResponse();
  }

  changeLeagueLineupSize(): void {
    this.currentPage = 1;
    this.fetchLeagueApiResponse();
  }

  applyFilter(): void {
    const search = this.searchTerm.trim().toLowerCase();

    if (!search) {
      this.filteredLineups = [...this.lineups];
    } else {
      this.filteredLineups = this.lineups.filter((lineup) =>
        lineup.players.some((player) =>
          player.name.toLowerCase().includes(search),
        ),
      );
    }

    this.currentPage = 1;
    this.sortLineups();
    this.updatePagination();
  }

  sortBy(column: keyof Lineup): void {
    if (this.sortColumn === column) {
      this.sortAscending = !this.sortAscending;
    } else {
      this.sortColumn = column;
      this.sortAscending = false;
    }

    this.currentPage = 1;
    this.sortLineups();
    this.updatePagination();
  }

  getPlayerNames(lineup: Lineup): string {
    return lineup.players
      .map((player) => player.name)
      .join(' • ');
  }

  trackByLineup(index: number, lineup: Lineup): string {
    return (
      lineup.players.map((player) => player.player_id).join('-') ||
      String(index)
    );
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updatePagination();
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updatePagination();
    }
  }

  private fetchLeagueApiResponse(): void {
    this.loading = true;
    this.errorMessage = '';

    this.lineupsService
      .getLineupsLeagueSummary(this.leagueLineupSize)
      .subscribe({
        next: (data) => {
          this.lineups = (data.apiResponse as Lineup[]) ?? [];

          // Calculate top five only when new API data arrives.
          this.topLineups = [...this.lineups]
            .filter((lineup) => lineup.total_possessions >= 10)
            .sort((a, b) => {
              if (b.net_rating !== a.net_rating) {
                return b.net_rating - a.net_rating;
              }

              return b.total_possessions - a.total_possessions;
            })
            .slice(0, 5);

          this.filteredLineups = [...this.lineups];

          this.searchTerm = '';
          this.currentPage = 1;
          this.sortColumn = 'net_rating';
          this.sortAscending = false;

          this.sortLineups();
          this.updatePagination();

          this.loading = false;
          this.cdr.markForCheck();
        },

        error: () => {
          this.lineups = [];
          this.filteredLineups = [];
          this.paginatedLineups = [];
          this.topLineups = [];

          this.currentPage = 1;
          this.totalPages = 1;
          this.loading = false;

          this.errorMessage =
            'Unable to load lineup data. Make sure the backend is running.';

          this.cdr.markForCheck();
        },
      });
  }

  private sortLineups(): void {
    const column = this.sortColumn;

    this.filteredLineups.sort((a, b) => {
      const aValue = Number(a[column]) || 0;
      const bValue = Number(b[column]) || 0;

      return this.sortAscending
        ? aValue - bValue
        : bValue - aValue;
    });
  }

  private updatePagination(): void {
    this.totalPages = Math.max(
      1,
      Math.ceil(this.filteredLineups.length / this.pageSize),
    );

    if (this.currentPage > this.totalPages) {
      this.currentPage = this.totalPages;
    }

    const start = (this.currentPage - 1) * this.pageSize;

    this.paginatedLineups = this.filteredLineups.slice(
      start,
      start + this.pageSize,
    );

    this.cdr.markForCheck();
  }
}